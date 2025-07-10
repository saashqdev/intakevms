How To Contribute
-----------------

1. [Establish a project.](README.md)


2. Find your task in
[issues](https://github.com/saashqdev/intakevms/issues).
If it is not there, then discuss it with the developers and after communication create a task in
[issues](https://github.com/saashqdev/intakevms/issues).

> We follow the *gitlab flow* methodology, so the next steps will be based on this methodology.

3. At this stage, a new branch is created in the *Github* repository to develop new functionality or fix a bug. The branch is created from the latest version of the *main* branch. The branch name should reflect its content and purpose. Here are some tips for a good branch name:
    - Use descriptive and easy-to-understand names. The branch name should clearly convey its content and purpose, so that other project participants can quickly understand
what it contains.
    - Use a notation that is understandable to all project participants. Good branch naming formats include *"feature/feature_name"*, *"bugfix/bug_fix_name"*, *"hotfix/hot_fix_name"*.
    - Try to keep thread names short and descriptive. Use no more than 3-4 words to describe the thread's content.
    - Use present tense verbs. This will help convey the idea that the branch represents ongoing work being done within the project.
    - Be consistent in branch naming. Try to use the same notation and naming style for all branches in your project.

    For example, if you are creating a branch for a new feature, then its name might be *"feature/add-user-profile"*. If you are fixing a bug, the branch name might be
    *"bugfix/fix-login-error"*. In both cases, the name reflects the content and purpose of the branch.


5. *Commit*: This is where the changes are committed to the created branch. Developers commit the changes to their local repositories and push them to the *GitLab* branch.
Here are some tips on how to write a commit message correctly:

  - Be concise and clear: The commit message should be short and descriptive enough that you can quickly understand what was changed in the commit. The goal is that other developers can quickly understand what was done without having to look through the entire code.
  - Use imperative verbs: It is best to use imperative verbs, such as "Add", "Delete", "Amend", "Update", to make the commit message clearer and more precise.
  - Remember the writing rules: The commit message should be grammatically correct and follow the writing standards.
  - Use capital letters and punctuation: The commit message must be formatted as a capitalized sentence and must end with a period.
  - Include the task number in the commit message. This will help you track which tasks were implemented in each commit.
  - Feel free to use a long description.  If you need to further describe the changes made in a commit, you can add a long description after the main commit message, separated by a blank line.

    For example, a good commit message might look like this:

    > Copy code
    >
    > To fix the error of validating the login form, an additional condition has been added to verify that the email field is filled in correctly.

    This quickly and clearly explains what was fixed in this commit.


6. Launching *unit* tests and running tests according to pep8.
Will be added in the future. Also in the project we adhere to
[google style guide](https://google.github.io/styleguide/pyguide.html).


7. Creating a *merge request*, here are some tips on formatting *Merge Requests*:

    - Give your *Merge Request'* a clear name: The name should reflect the nature of the changes you are making to the code. The name should be short but descriptive, so that other developers can quickly understand what was done.
    - Add a description to the *Merge Request*: The description should contain detailed information about what was changed, why the changes were made, and any other additional details that may help other developers understand the changes.
    - Before you create a *Merge Request*, make sure that your changes are tested. This will help to ensure that your code works correctly and does not introduce new problems.
    - Specify which tasks the *Merge Request* applies to. This will help track which tasks have been implemented in this *Merge Request*.
    - Explain how other developers can review your changes: Include instructions on how other developers can review your code. Make sure the instructions are clear and precise.
    - Leave comments and interact with other developers: If other developers leave comments or suggest changes, feel free to interact with them and respond to their comments.

    Design example *Merge Request*:

    Title: Add functionality to send email

    Description:
     * Added new function for sending emails.
     * Updated controllers and models to support new functionality.
     * Added tests to check new functionality.
     * The documentation has been updated to reflect the new features.

   Tasks:
     * issues-3
     * issues-4

   Instructions for checking:
     * Download the *feature/email* branch and run the application on your local server.
     * Send a test email and make sure everything works correctly.
  
   Comments:
     * Please make sure you have updated the document.


9. Then *CI/CD* is automatically launched and run
   *smoke tests*.


10. Afterwards, a *code review* is performed and if successful, the branch is merged.
