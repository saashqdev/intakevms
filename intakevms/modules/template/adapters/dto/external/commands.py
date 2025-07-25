"""DTOs for external service-layer command requests.

This module provides typed command DTOs used for RPC-based communication with
external systems, such as volume and storage services.
"""

from uuid import UUID

from intakevms.common.base_pydantic_models import BaseDTOModel


class GetVolumeCommandDTO(BaseDTOModel):
    """DTO for querying a volume by its ID.

    This model is used to create a JSON-serializable payload for RPC calls
    that require a volume identifier. It leverages the JSON encoders defined
    in DTOConfig to automatically convert UUID values to strings.

    Attributes:
        volume_id (UUID): Unique identifier of the volume.

    Example:
        >>> from uuid import UUID
        >>> query = VolumeQuery(volume_id=UUID('123e4567-e89b-12d3-a456-426614174000'))
        >>> payload = query.model_dump(mode='json')
        >>> print(payload)  # {'volume_id': '123e4567-e89b-12d3-a456-426614174000'}
    """  # noqa: E501

    volume_id: UUID


class GetStorageCommandDTO(BaseDTOModel):
    """DTO for querying a storage by its ID.

    This model is used to create a JSON-serializable payload for RPC calls
    that require a storage identifier. It leverages the JSON encoders defined
    in DTOConfig to automatically convert UUID values to strings.

    Attributes:
        storage_id (UUID): Unique identifier of the volume.

    Example:
        >>> from uuid import UUID
        >>> query = VolumeQuery(storage_id=UUID('123e4567-e89b-12d3-a456-426614174000'))
        >>> payload = query.model_dump(mode='json')
        >>> print(payload)  # {'storage_id': '123e4567-e89b-12d3-a456-426614174000'}
    """  # noqa: E501

    storage_id: UUID


class GetVmCommandDTO(BaseDTOModel):
    """DTO for querying a virtual machine by its ID.

    This model is used to create a JSON-serializable payload for RPC calls
    that require a virtual machine identifier. It leverages the JSON encoders
    defined in DTOConfig to automatically convert UUID values to strings.

    Attributes:
        vm_id (UUID): Unique identifier of the virtual machine.

    Example:
        >>> from uuid import UUID
        >>> query = GetVmCommandDTO(vm_id=UUID('123e4567-e89b-12d3-a456-426614174000'))
        >>> payload = query.model_dump(mode='json')
        >>> print(payload)  # {'vm_id': '123e4567-e89b-12d3-a456-426614174000'}
    """  # noqa: E501

    vm_id: UUID