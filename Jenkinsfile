pipeline {
    agent any

    environment {
        DOCKER_HOST = 'tcp://docker-ci:2375'
    }

    stages {
        stage('Installation et vérification') {
            steps {
                sh '''
                    set -e
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install -r backend/requirements.txt
                    python -m py_compile backend/main.py
                '''
            }
        }

        stage('Tests de connexion') {
            steps {
                sh '''#!/bin/sh
set -e
. .venv/bin/activate

python - <<'PY'
from fastapi import HTTPException
from backend.main import UserLogin, login

result = login(UserLogin(email="admin@smartcampus.ma", password="password123"))
assert result["status"] == "success"

try:
    login(UserLogin(email="admin@smartcampus.ma", password="incorrect"))
except HTTPException as error:
    assert error.status_code == 401
else:
    raise AssertionError("La connexion incorrecte aurait dû être refusée")

print("Tests de connexion réussis")
PY
'''
            }
        }

        stage('Construction Docker') {
            steps {
                sh '''
                    set -e
                    docker version
                    docker build -t smartcampus:jenkins .
                    docker image ls smartcampus
                '''
            }
        }
    }
}