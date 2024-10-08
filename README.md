# CTCTLab

## Table of Contents

1. [Introduction](#introduction)
2. [Backend - Django](#backend---django)
   1. [Setup and Installation](#setup-and-installation)
   2. [Models](#models)
   3. [Serializers](#serializers)
   4. [Views](#views)
   5. [URLs Configuration](#urls-configuration)
   6. [Authentication and Permissions](#authentication-and-permissions)
   7. [API Endpoints](#api-endpoints)
3. [Frontend - VueJS](#frontend---vuejs)
   1. [Project Setup](#project-setup)
   2. [Components](#components)
   3. [Vuex Store](#vuex-store)
   4. [Router Configuration](#router-configuration)
   5. [Axios Configuration](#axios-configuration)
   6. [Styling and Layout](#styling-and-layout)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

This project is a comprehensive web application designed to facilitate the interactive and dynamic learning experience in educational environments. It integrates a Django-based backend with a VueJS frontend, offering a seamless, responsive, and user-friendly interface for both students and educators.

Key features of this application include:

- **Dynamic Questionnaires**: Enables the creation and distribution of questionnaires for educational purposes.
- **User Profiles**: Supports distinct user profiles for students and teachers, each with tailored functionalities.
- **Real-Time Analytics**: Provides real-time insights into student performance and questionnaire responses.
- **Interactive Learning Modules**: Includes various modules like `WeekComponent`, `TPClassesComponent`, and `QuestionsComponent`, enhancing the learning experience.
- **Secure Authentication**: Utilizes robust authentication mechanisms to ensure data security and user privacy.
- **Responsive Design**: Crafted with a responsive design, ensuring compatibility across various devices and screen sizes.

The backend is built using Django, a high-level Python web framework that encourages rapid development and clean, pragmatic design. The frontend is developed with VueJS, a progressive JavaScript framework used for building user interfaces and single-page applications. The application is designed with scalability in mind, ensuring that it can easily adapt to the growing needs of educational institutions.

## Backend - Django

### Setup and Installation

The CTCTLab project's Django backend is configured with an emphasis on security, performance, and cross-platform compatibility. Here are the key setup and installation details:

- **Django Version**: The project uses Django 5.0, which is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Environment Variables**: The project utilizes environment variables for configuration settings like `SECRET_KEY`, database credentials, and email backend configurations. This is facilitated through the `dotenv` package, which loads variables from a `.env` file into `os.environ`.

- **Base Directory**: The `BASE_DIR` in `settings.py` is set to the directory where the `manage.py` file exists, serving as the root directory for the Django project.

- **Security Settings**:

  - `SECRET_KEY`: Pulled from the environment variables for security.
  - `DEBUG`: Controlled via environment variables. It's set to `True` by default but should be set to `False` in production.
  - `ALLOWED_HOSTS`: Includes development and production hosts.

- **Installed Apps**: Includes Django's default apps along with `corsheaders`, `rest_framework`, `rest_framework.authtoken`, `dj_rest_auth`, and `rest_framework_simplejwt`. The project-specific apps like `users`, `questions`, and `analytics` are also listed.

- **Middleware Configuration**: Uses standard Django middleware along with `CorsMiddleware` for handling Cross-Origin Resource Sharing (CORS).

- **Database Configuration**:

  - Engine: MySQL
  - Name, User, Password, Host, and Port are configured through environment variables.
  - Specific database options can also be set, such as SQL mode.

- **Email Backend Configuration**:

  - Uses SMTP with Gmail.
  - Email settings (like host, port, and credentials) are pulled from environment variables.

- **Authentication and Password Validation**:

  - Custom password validators are used for enhanced security.
  - Utilizes JSON Web Tokens (JWT) for authentication via `rest_framework_simplejwt`.

- **Internationalization**:

  - Language code is set to `pt-pt`, and time zone is set to `Europe/Lisbon`.
  - Supports internationalization and timezone settings.

- **Static and Media Files**:

  - Configures the URLs and root directories for static and media files.
  - Includes settings to integrate with the VueJS frontend.

- **Cross-Origin Resource Sharing (CORS)**:
  - Configured to allow requests from specific origins, particularly the VueJS frontend running on localhost (ports 8080 and 8081).

This configuration ensures that the Django backend is robust, secure, and ready to integrate with the VueJS frontend.

### Models

The CTCTLab project uses a range of Django models to represent different entities in the application. These models are integral to the application's functionality, providing the necessary data structures for users, courses, classrooms, activities, questionnaires, and more.

#### Users Application Models

1. **User (Custom User Model)**:

   - Inherits from `AbstractUser`.
   - Fields:
     - `is_student`: Boolean field to identify if the user is a student.
     - `is_teacher`: Boolean field to identify if the user is a teacher.

2. **Course**:

   - Represents an academic course.
   - Fields:
     - `name`: CharField to store the unique name of the course.

3. **Classroom**:

   - Represents a classroom.
   - Fields:
     - `name`: CharField for the classroom name.
     - `capacity`: IntegerField for the classroom capacity, nullable.
     - `class_type`: CharField for the type of class (e.g., Theoretical-Practical, Practical).

4. **StudentProfile**:

   - Extended model for a student, linked to the User model.
   - Fields:
     - `user`: OneToOneField linking to the User model.
     - `classroom`: ForeignKey linking to the Classroom model.
     - `student_number`: IntegerField for a unique student number.
     - `course`: ForeignKey linking to the Course model.
     - `age`: IntegerField for the student's age.
     - `gender`: CharField for the student's gender.
     - `data_consent`: BooleanField for consent to data usage.

5. **TeacherProfile**:

   - Extended model for a teacher, linked to the User model.
   - Fields:
     - `user`: OneToOneField linking to the User model.
     - `classrooms`: ManyToManyField linking to multiple Classroom models.

6. **StudentGroup**:
   - Model representing groups of students.
   - Fields:
     - `students`: ManyToManyField linking to StudentProfile models.
     - `classroom`: ForeignKey linking to the Classroom model.
     - `week`: ForeignKey linking to the Week model from the questions application.

#### Questions Application Models

1. **Week**:

   - Represents an academic week.
   - Fields:
     - `number`: IntegerField for the week number.
     - `theme`: CharField for the week's theme.
     - `start_date`: DateField for the start date.
     - `end_date`: DateField for the end date.
     - `description`: TextField for the week's description.

2. **Activity**:

   - Represents an academic activity.
   - Fields:
     - `title`: CharField for the activity title.
     - `description`: TextField for the activity description.
     - `week`: ForeignKey linking to the Week model.

3. **ActivityInstance**:

   - Represents an instance of an activity.
   - Fields:
     - `activity`: ForeignKey linking to the Activity model.
     - `classroom`: ForeignKey linking to the Classroom model.
     - `start_time`: DateTimeField for the start time of the activity.
     - `end_time`: DateTimeField for the end time of the activity.
     - `is_active`: BooleanField indicating if the activity is active.

4. **Questionnaire**:

   - Represents a questionnaire.
   - Fields:
     - `title`: CharField for the questionnaire title.
     - `description`: TextField for the questionnaire description.
     - `questions`: ManyToManyField linking to Question models.
     - `activity`: ForeignKey linking to the Activity model, nullable.

5. **Question**:

   - Represents a question within a questionnaire.
   - Fields:
     - `question_text`: CharField for the question text.
     - `question_type`: CharField for the type of question (e.g., MCQ, True/False).
     - `questionnaire`: ForeignKey linking to the Questionnaire model.

6. **Option**:

   - Represents an option for a question.
   - Fields:
     - `question`: ForeignKey linking to the Question model.
     - `option_text`: CharField for the option text.
     - `is_correct`: BooleanField indicating if the option is correct.

7. **QuestionnaireQuestion**:

   - Intermediate model to define the order of questions in a questionnaire.
   - Fields:
     - `questionnaire`: ForeignKey linking to the Questionnaire model.
     - `question`: ForeignKey linking to the Question model.
     - `order`: PositiveIntegerField for the order of the question.

8. **StudentQuestionnaireResponse**:

   - Model to record a student's overall response to a questionnaire.
   - Fields:
     - `student`: ForeignKey linking to the StudentProfile model.
     - `questionnaire`: ForeignKey linking to the Questionnaire model.
     - `answered_on`: DateTimeField for the time when the response is created.

9. **QuestionResponseDetail**:
   - Model to store detailed responses of a student to each question.
   - Fields:
     - `student_response`: ForeignKey linking to the StudentQuestionnaireResponse model.
     - `question`: ForeignKey linking to the Question model.
     - `selected_option`: ForeignKey linking to the Option model.
     - `is_correct`: BooleanField set based on the selected option's correctness.

These models form the backbone of the CTCTLab's data structure, supporting its functionalities and representing the core aspects of the application, from user management to the dynamic creation and handling of educational content.

Documentation of Django models, detailing each model's fields, relationships, and purpose.

### Serializers

Serializers in the CTCTLab project play a crucial role in converting complex data types, such as querysets and model instances, to and from JSON format. This facilitates the communication between the Django backend and the VueJS frontend.

1. **UserSerializer**:

   - **Purpose**: Serializes the custom User model.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `username`: Username of the user.
     - `email`: Email address of the user.
     - `is_student`: Boolean to identify if the user is a student.
     - `is_teacher`: Boolean to identify if the user is a teacher.

2. **StudentProfileSerializer**:

   - **Purpose**: Serializes the StudentProfile model with nested user data.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `user`: Nested UserSerializer.
     - `student_number`: Unique student number.
     - `course`: ForeignKey to the Course model.
     - `age`: Age of the student.
     - `gender`: Gender of the student.
     - `data_consent`: Boolean for data usage consent.
     - `tp_classroom`: SlugRelatedField to the Classroom model.

3. **TeacherProfileSerializer**:

   - **Purpose**: Serializes TeacherProfile model with nested user data and associated classrooms.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `user`: Nested UserSerializer.
     - `classrooms`: ManyToManyField with Classroom model, represented with slug names.

4. **CourseSerializer**:

   - **Purpose**: Used for serializing the Course model.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `name`: Name of the course.

5. **StudentGroupSerializer**:

   - **Purpose**: Serializes the StudentGroup model with nested student profiles.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `students`: ManyToManyField with StudentProfile model, represented with nested serializers.
     - `classroom`: ForeignKey to the Classroom model.
     - `week`: ForeignKey to the Week model.

6. **CustomLoginSerializer**:

   - **Purpose**: Custom serializer for handling login requests.
   - **Fields**:
     - `username`: Username of the user.
     - `password`: Password of the user, represented with password style input.

7. **UserAndProfileRegistrationSerializer**:

   - **Purpose**: Handles registration of both User and StudentProfile models.
   - **Fields**:
     - User model related fields: `username`, `password`, `email`, `first_name`, `last_name`.
     - StudentProfile model related fields: `course`, `age`, `gender`, `data_consent`.
   - **Create Method**: Validates data, creates User instance, and links it with a StudentProfile instance.

8. **ClassroomSerializer**:
   - **Purpose**: Serializes Classroom model.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `name`: Name of the classroom.
     - `capacity`: Capacity of the classroom.
     - `class_type`: Type of class (TP or P).
     - `class_type_display`: Human-readable representation of class_type.

### Serializers

Serializers in the CTCTLab project play a crucial role in converting complex data types, such as querysets and model instances, to and from JSON format. This facilitates the communication between the Django backend and the VueJS frontend.

1. **UserSerializer**:

   - **Purpose**: Serializes the custom User model.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `username`: Username of the user.
     - `email`: Email address of the user.
     - `is_student`: Boolean to identify if the user is a student.
     - `is_teacher`: Boolean to identify if the user is a teacher.

2. **StudentProfileSerializer**:

   - **Purpose**: Serializes the StudentProfile model with nested user data.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `user`: Nested UserSerializer.
     - `student_number`: Unique student number.
     - `course`: ForeignKey to the Course model.
     - `age`: Age of the student.
     - `gender`: Gender of the student.
     - `data_consent`: Boolean for data usage consent.
     - `tp_classroom`: SlugRelatedField to the Classroom model.

3. **TeacherProfileSerializer**:

   - **Purpose**: Serializes TeacherProfile model with nested user data and associated classrooms.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `user`: Nested UserSerializer.
     - `classrooms`: ManyToManyField with Classroom model, represented with slug names.

4. **CourseSerializer**:

   - **Purpose**: Used for serializing the Course model.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `name`: Name of the course.

5. **StudentGroupSerializer**:

   - **Purpose**: Serializes the StudentGroup model with nested student profiles.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `students`: ManyToManyField with StudentProfile model, represented with nested serializers.
     - `classroom`: ForeignKey to the Classroom model.
     - `week`: ForeignKey to the Week model.

6. **CustomLoginSerializer**:

   - **Purpose**: Custom serializer for handling login requests.
   - **Fields**:
     - `username`: Username of the user.
     - `password`: Password of the user, represented with password style input.

7. **UserAndProfileRegistrationSerializer**:

   - **Purpose**: Handles registration of both User and StudentProfile models.
   - **Fields**:
     - User model related fields: `username`, `password`, `email`, `first_name`, `last_name`.
     - StudentProfile model related fields: `course`, `age`, `gender`, `data_consent`.
   - **Create Method**: Validates data, creates User instance, and links it with a StudentProfile instance.

8. **ClassroomSerializer**:
   - **Purpose**: Serializes Classroom model.
   - **Fields**:
     - `id`: AutoField, primary key.
     - `name`: Name of the classroom.
     - `capacity`: Capacity of the classroom.
     - `class_type`: Type of class (TP or P).
     - `class_type_display`: Human-readable representation of class_type.

### URLs Configuration

The URLs in CTCTLab are configured to route requests to appropriate views. Here's a breakdown of the URLs configuration across different applications:

#### Main URL Configuration (ctct_api/urls.py)

- **Admin**:
  - Route: `admin/`
  - Connects to Django's admin interface.
- **Users Application**:
  - Route: `api/users/`
  - Includes URLs from the `users` application.
- **Questions Application**:
  - Route: `api/questions/`
  - Includes URLs from the `questions` application.

#### Questions Application URLs (questions/urls.py)

- Utilizes a router to register various viewsets for models like Activity, ActivityInstance, Week, Questionnaire, etc.
- Custom routes:
  - `activities/<int:activity_id>/questionnaires/`: Retrieves questionnaires for a specific activity.
  - `create_student_responses/`: Endpoint for creating student responses.
  - `stats/`: Endpoint for question statistics.
  - `opt_dist/`: Endpoint for option distribution.
  - `last_answered_questionnaire/`: Retrieves the last answered questionnaire.

#### Users Application URLs (users/urls.py)

- Utilizes a router to register viewsets for models such as User, Course, Classroom, StudentProfile, etc.
- Custom routes:
  - `login/`: Endpoint for user login.
  - `logout/`: Endpoint for user logout.
  - `currentUser/`: Retrieves the current user's information.
  - `token/`: Endpoint for obtaining JWT tokens.
  - `token/refresh/`: Endpoint for refreshing JWT tokens.
  - `activate/<uidb64>/<token>/`: Endpoint for account activation.

### Authentication and Permissions

CTCTLab uses JSON Web Tokens (JWT) for authentication, ensuring secure access to the application's features.

- **Custom User Model**:
  - Defined as `'users.User'`.
- **Authentication Classes**:
  - The project uses `'rest_framework_simplejwt.authentication.JWTAuthentication'` as the default authentication class.
- **JWT Configuration**:
  - **Algorithm**: HS256.
  - **Signing Key**: Derived from the project's `SECRET_KEY`.
  - **Token Lifespan**: Access tokens have a lifetime of 120 minutes, while refresh tokens last for 1 day.

### API Endpoints

The CTCTLab project offers various API endpoints, each corresponding to specific functionalities:

- **Activity**:
  - CRUD operations for activities.
  - Endpoint: `activity/`.
- **Activity Instance**:
  - CRUD operations for activity instances.
  - Endpoint: `activityinstance/`.
- **Week**:
  - CRUD operations for weeks.
  - Endpoint: `weeks/`.
- **Questionnaire**:
  - CRUD operations for questionnaires.
  - Endpoint: `questionnaires/`.
- **Question**:
  - CRUD operations for questions.
  - Endpoint: `questions/`.
- **Option**:
  - CRUD operations for options.
  - Endpoint: `options/`.
- **QuestionnaireQuestion**:
  - CRUD operations for questionnaire-question relations.
  - Endpoint: `questionnairequestions/`.
- **StudentQuestionnaireResponse**:
  - CRUD operations for student questionnaire responses.
  - Endpoint: `studentresponses/`.
- **QuestionResponseDetail**:
  - CRUD operations for question response details.
  - Endpoint: `questionresponsedetails/`.

Additional custom endpoints are also available for specific actions like creating student responses, obtaining question statistics, and more.

## Frontend - VueJS

The CTCTLab's frontend is built using VueJS, offering a dynamic and interactive user interface. This section outlines the setup, key components, state management via Vuex, routing with Vue Router, Axios configuration for API requests, styling guidelines, and deployment instructions.

### Project Setup

To set up the VueJS environment for the CTCTLab project, follow these steps:

1. **Install Node.js**: Ensure Node.js is installed on your machine. VueJS requires Node.js to run the development server and build the project.
2. **Install Vue CLI**: Use npm or yarn to install Vue CLI globally on your machine. Vue CLI is a powerful tool that facilitates the creation, development, and management of VueJS projects.
   > npm install -g @vue/cli  
   > yarn global add @vue/cli
3. **Create a Vue Project**: If starting from scratch, use Vue CLI to create a new project. For existing projects, skip to the next step.
   > vue create ctctlab-frontend
4. **Install Dependencies**: Navigate to the project directory and install the required dependencies.
   > cd ctctlab-frontend  
   > npm install

### Components

The CTCTLab frontend utilizes several Vue components for different parts of the application. Here's an overview of some key components and their functionalities:

- **HomePage.vue**: Serves as the landing page for the application.
- **LoginModal.vue**: A modal component for user login.
- **RegisterModal.vue**: Handles user registration.
- **NavbarComponent.vue**: Provides navigation across the application.
- **WeekComponent.vue**: Displays weekly content and activities.
- **QuestionsComponent.vue**: Manages the creation and display of questionnaires.

Each component is designed to be reusable and modular, facilitating ease of maintenance and development.

### Vuex Store

CTCTLab leverages Vuex for state management. The `store.js` file configures the Vuex store, defining the state, mutations, actions, and getters necessary for managing the application's state:

- **State**: Contains the application's state variables such as `currentUser`, `authToken`, and `answeredQuestionnaires`. The `currentUser` includes dynamically loaded profile IDs (`studentProfileId`, `teacherProfileId`) from local storage to maintain user state across sessions.

  ```javascript
  state: {
    currentUser: getSavedState("currentUser"),
    authToken: getSavedState("authToken"),
    answeredQuestionnaires: getSavedState("answeredQuestionnaires") || [],
  },
  ```

- **Mutations**: Functions to mutate the application's state directly. This includes setting the current user, updating profile IDs, managing the auth token, and handling answered questionnaires. Mutations ensure that state changes are trackable and predictable.

  ```javascript
  mutations: {
    setCurrentUser(state, userData) {...},
    setStudentProfileId(state, profileId) {...},
    setTeacherProfileId(state, profileId) {...},
    setAuthToken(state, token) {...},
    clearAuthData(state) {...},
    setAnsweredQuestionnaires(state, questionnaires) {...},
    addAnsweredQuestionnaire(state, questionnaireId) {...},
  },
  ```

- **Actions**: Asynchronous operations that commit mutations to the state. Actions include fetching user profiles based on the current user's role (student/teacher), updating the current user, handling login/logout processes, marking questionnaires as answered, and fetching answered questionnaires.

  ```javascript
  actions: {
    async fetchAndSetUserProfile({ commit, state }) {...},
    updateCurrentUser({ commit, dispatch }, userData) {...},
    updateAuthToken({ commit }, token) {...},
    logout({ commit }) {...},
    markQuestionnaireAsAnswered({ commit }, questionnaireId) {...},
    async fetchAnsweredQuestionnaires({ commit, state }) {...},
  },
  ```

- **Getters**: Compute derived state based on the store's state, allowing for easy access and manipulation of the state within components. Getters include methods to get the current user, check if a user is a student or teacher, access user profile IDs, and determine if a user is logged in or if a questionnaire has been answered.

  ```javascript
  getters: {
    getCurrentUser: (state) => state.currentUser,
    isStudent: (state) => state.currentUser?.is_student,
    isTeacher: (state) => state.currentUser?.is_teacher,
    getStudentNumber: (state) => state.currentUser?.studentNumber,
    getStudentProfileId: (state) => state.currentUser?.studentProfileId,
    getTeacherProfileId: (state) => state.currentUser?.teacherProfileId,
    isLoggedIn: (state) => !!state.authToken,
    getAuthToken: (state) => state.authToken,
    isQuestionnaireAnswered: (state) => (questionnaireId) => state.answeredQuestionnaires.includes(questionnaireId),
  },
  ```

This Vuex store setup allows the CTCTLab application to maintain a centralized and reactive state, ensuring that components can reactively and efficiently display data and respond to user interactions.

### Router Configuration

Vue Router is utilized for navigating between pages within the application. The `router.js` file outlines the routes and their corresponding components, along with navigation guards to handle authentication and redirect logic:

- **Routes**: Defines the path and component mappings for the application.
- **Navigation Guards**: Utilizes `beforeEach` to check for authentication before accessing certain routes.

### Axios Configuration

The `axiosConfig.js` file configures Axios for API requests, setting up base URLs, headers, and interceptors for request and response handling:

- **Base URL**: Specifies the API's base URL.
- **Headers**: Sets common headers for all requests, such as `Content-Type`.
- **Interceptors**: Adds request interceptors to include authentication tokens, and response interceptors to handle errors globally.

### Styling and Layout

CTCTLab uses Bootstrap for styling and layout, ensuring a responsive and user-friendly interface. Custom CSS can be added to individual components for specific styling needs.

### Testing

Testing is conducted using Vue Test Utils and Jest. Tests for components ensure functionality is as expected and document how components are supposed to be used.

### Deployment

Deployment instructions would include building the VueJS project for production and deploying it to a web server or a service like Netlify or Vercel.

### Contributing

Guidelines for contributing to the CTCTLab project, including code style, branching strategy, and pull request process.

### License

State the project's license and terms of use.
