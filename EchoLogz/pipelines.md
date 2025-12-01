# EchoLogz System Pipelines


# ----------------------------------------------------------------------------------------
## Signup (Account Creation) Pipeline 
# ----------------------------------------------------------------------------------------

### Goal

Create a new EchoLogz user account, store it in the database with a
securely hashed password, and return a JWT so the frontend can move
into the email verification / onboarding flow.

---

## Modules Touched by the Signup Pipeline

### Frontend Modules
- `frontend-react/src/SignUp.jsx`
- `frontend-react/src/components/AccountStep.jsx`
- `frontend-react/src/components/CodeStep.jsx`
- `frontend-react/src/utils.js` *(password / email format checks)*

#### Structural Only
- `frontend-react/src/App.jsx` *(only bc routes to SignUp)*

# UI Components (Rendered but not logically involved)
- `frontend-react/index.html` *(root mount point, passive)*
- `frontend-react/components/Navbar.jsx`
- `frontend-react/components/StepIndicator.jsx`
- `frontend-react/src/pw-style.css` *(styling only)*

### Backend Modules

#### FastAPI App + Routing
- `backend/main.py`
- `backend/routers/r_auth.py`

#### Request / Response Schemas
- `backend/echoDB/db_schemas_api.py`

#### Database / Returned info
- `backend/echoDB/db_session.py`
- `backend/echoDB/db_schemas.py`
- `backend/echoDB/db_users.py`

#### Security (Hashing + JWT)
- `backend/core/security.py`
- `backend/core/security_jwt.py`
- `backend/core/config.py` *(if JWT settings or secrets come from here)*

#### Database Storage (Physical)
- `backend/echoDB/echoDB.sqlite`



### Frontend flow

1. User opens the signup page

   - File: `frontend-react/src/SignUp.jsx`
   - Manages:
     - `step` (1 = Account, 2 = Verify)
     - `loading`
     - `signupEmail`
     - any error state

2. User fills out account form

   - File: `frontend-react/src/components/AccountStep.jsx`
   - Collects:
     - `username`
     - `email`
     - `password`
     - `confirmPassword`
   - On submit:
     - Runs basic client-side checks (ex: if passwords match)
     - Calls a submit handler passed in from `SignUp.jsx`

3. Frontend sends signup request

   - File: `frontend-react/src/SignUp.jsx`
   - Builds JSON body:
     ```json
     {
       "email": "<string>",
       "password": "<string>"
     }
     ```
   - Sends `POST /auth/signup` to the backend (using `fetch`).
   - Sets `loading = true` while the request is in flight.

4. Frontend handles signup response

    On success:
    - The backend returns JSON shaped like:
    ```json
    {
    "user": {
        "email": "<string>"
    },
    "verify_token": "<string>",
    "verify_expires_in": <number>
    }
    ```
    - Updates `step` from 1 → 2 to show the Verify Email step
    (`CodeStep.jsx`).
    - On failure:
        - Reads error `detail` from the response.
        - Updates error state in `SignUp.jsx` so `AccountStep.jsx` can
        show the error message to the user.

5. Transition to Verify step

    - File: `frontend-react/src/components/CodeStep.jsx`
    - Receives `email`, `verifyToken`, and `verifyExpiresIn` from `onSignupSuccess(...)`,
    which was populated from the backend response (`data.user.email`, `data.verify_token`, etc.).
    - Displays the user’s email to confirm where the verification link was sent.
    - Shows instructions:
        - Password expires in...
        - “Check your email / dev link in terminal.”
        - Provides a button to continue onboarding (and later, a “Resend verification link” button).

---

### Backend flow

1. Request hits FastAPI app

   - File: `backend/main.py`
   - App setup includes the auth router:
     ```python
     app.include_router(r_auth.router)
     ```
   - The request `POST /auth/signup` is routed to the auth module.

2. Signup endpoint receives data

   - File: `backend/routers/r_auth.py`
   - Endpoint:
     ```python
     @router.post("/signup",
                  response_model=SignupOut, status_code=201)
     def signup_user(payload: UserCreate, background:BackgroundTasks,
                     db: Session = Depends(get_db)):
         ...
     ```
   - `payload` is a Pydantic model (`db_schemas.py`) that validates incoming JSON.

3. Request schema validation

   - File: `backend/echoDB/db_schemas.py`
   - Model:
     ```python
     class SignupOut(BaseModel):
         user: UserOut
         verify_token: str
         verify_expires_in: int
     ```
   - FastAPI converts the incoming JSON into `SignupOut` and
     rejects invalid data with a 422 standard FastAPI response (Uprocessable Entity).

4. Database session is created

   - File: `backend/echoDB/db_session.py`
   - Dependency:
     ```python
     def get_db():
         db = SessionLocal()
         try:
             yield db
         finally:
             db.close()
     ```
   - `db` is an active SQLAlchemy session connected to the SQLite
     database.

5. Password is hashed

   - File: `backend/core/security.py`
   - Function:
     ```python
     hashed = security._hash_password(payload.password)
     ```
   - Uses `passlib` (`bcrypt`) to turn the plain-text password
     into a secure hash that is safe to store in the database.

6. User ORM object is created and saved

   - Files:
     - `backend/echoDB/db_schemas.py` (SQLAlchemy models)
     - `backend/echoDB/db_crud.py` (db operations)
     - `backend/echoDB/db_tables.py` (ORM models)

   - ORM model:
     ```python
     class User(Base):
         __tablename__ = "users"

         id = Column(Integer, primary_key=True, index=True)
         email = Column(String, unique=True, nullable=False)
         hashed_password = Column(String, nullable=False)
         is_verified = Column(Boolean, nullable=False, default=False)
         # Link to SpotifyAccount rows
         spotify_accounts = relationship(
            "SpotifyAccount",
            back_populates="user",
            cascade="all, delete-orphan",
            passive_deletes=True,
         )
     ```
   - Creation helper (`db_crud.py`):
     ```python
     user = create_user_with_hash(
         db=db,
         username=payload.username,
         email=payload.email,
         hashed_pw=hashed_pw,
     )
     ```
   - This function:
     - Builds a `User` instance
     - `db.add(user)`
     - `db.commit()` (writes the row)
     - `db.refresh(user)` (loads DB-assigned fields like `id`)
   - If constraints fail (e.g. duplicate username/email), the DB raises
     an error that is caught and turned into an HTTP error response.

7. JWT access token is generated

   - File: `backend/core/security_jwt.py`
   - Function:
     ```python
     access_token = create_access_token(
         data={"sub": str(user.id)},
         expires_delta=timedelta(minutes=60),
     )
     ```
   - The token encodes:
     - user id (subject)
     - expiry timestamp
   - Signed with the app’s secret key and algorithm.

8. Response schema and return

   - File: `backend/echoDB/db_schemas_api.py`
   - Model:
     ```python
     class TokenOut(BaseModel):
         access_token: str
         token_type: str = "bearer"
     ```
   - Endpoint returns:
     ```python
     return TokenOut(access_token=access_token)
     ```
   - FastAPI serializes this to JSON and sends it back to the
     frontend.

---

### Summary (Signup Pipeline in one line)

**Frontend** collects account info → sends `POST /auth/signup` →  
**Backend** validates, hashes password, saves new `User`, creates JWT →  
returns `{ access_token, token_type }` → **Frontend** stores token,
keeps `signupEmail`, and moves the user into the verification step.



# ----------------------------------------------------------------------------------------
## JWT Validation Pipeline
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
## Login Pipeline
# ----------------------------------------------------------------------------------------
(… next …)

# ----------------------------------------------------------------------------------------
## Spotify OAuth Pipeline
# ----------------------------------------------------------------------------------------
(… later …)

# ----------------------------------------------------------------------------------------
## Match Score Computation Pipeline
# ----------------------------------------------------------------------------------------
(… later …)

# ----------------------------------------------------------------------------------------
## History Page Pipelines
# ----------------------------------------------------------------------------------------
