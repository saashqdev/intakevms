"""Module for handling event-related API endpoints.

This module defines the FastAPI router and endpoint for retrieving events.
It uses the `EventCrud` class for database interactions and includes user
authentication dependencies.

Attributes:
    LOG (Logger): Logger instance for logging events in the module.
    router (APIRouter): FastAPI router for event-related endpoints.
"""

import io
import csv
from typing import List, cast

from fastapi import Depends, APIRouter, status
from fastapi.responses import StreamingResponse
from fastapi_pagination import Page, Params, paginate

from intakevms.libs.log import get_logger
from intakevms.libs.auth.jwt_utils import get_current_user
from intakevms.modules.event_store.entrypoints import schemas
from intakevms.modules.event_store.entrypoints.crud import EventCrud

LOG = get_logger(__name__)

router = APIRouter(
    prefix='/event',
    tags=['event'],
    responses={404: {'description': 'Not found!'}},
)


@router.get(
    '/',
    response_model=Page[schemas.Event],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_events(
    crud: EventCrud = Depends(EventCrud),
) -> Page[schemas.Event]:
    """Retrieve all events from the database.

    This endpoint retrieves all events using the EventCrud class and returns
    them in a paginated format.

    Args:
        crud (EventCrud): Instance of EventCrud for database operations.

    Returns:
        Page[schemas.Event]: A paginated list of events.

    Raises:
        HTTPException: If any database error occurs or events are not found.
    """
    result: List = crud.new_get_all_events()
    return cast(Page, paginate(result))


@router.get(
    '/download',
    response_model=schemas.DownloadResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def download_events(
    crud: EventCrud = Depends(EventCrud),
) -> StreamingResponse:
    """Download all events as a CSV file.

    This endpoint retrieves all events using the EventCrud class, generates
    a CSV file containing the event data, and returns it as a streaming
    response.

    Args:
        crud (EventCrud): Instance of EventCrud for database operations.

    Returns:
        StreamingResponse: A streaming response with the CSV file content.
    """
    result: List = crud.new_get_all_events()
    events_page: Page = paginate(
        result, params=Params(page=1, size=len(result))
    )

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # We write down the headings
    writer.writerow(
        [
            'id',
            'module',
            'object_id',
            'user_id',
            'event',
            'timestamp',
            'information',
        ]
    )

    # Recording data
    for event in events_page.items:
        writer.writerow(
            [
                event['id'],
                event['module'],
                event['object_id'],
                event['user_id'],
                event['event'],
                event['timestamp'],
                event['information'],
            ]
        )

    output.seek(0)

    return StreamingResponse(
        output,
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=logs.csv'},
    )