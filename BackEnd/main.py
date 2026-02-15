from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database
from exceptions.global_exception_handler import global_exception_handler
from routers import competence_router, language_router, training_router, position_router, department_router, \
    worker_router

app = FastAPI()

origins = [
    'http://localhost:5173',
    'http://localhost:5174'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.Base.metadata.create_all(bind=database.engine)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(competence_router.router, prefix="/competence", tags=["competence"])
app.include_router(language_router.router, prefix="/language", tags=["language"])
app.include_router(training_router.router, prefix="/training", tags=["training"])
app.include_router(position_router.router, prefix="/position", tags=["position"])
app.include_router(department_router.router, prefix="/department", tags=["department"])
app.include_router(worker_router.router, prefix="/worker", tags=["worker"])