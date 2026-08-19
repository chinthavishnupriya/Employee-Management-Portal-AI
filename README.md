AI-Powered Employee Management Portal

Project Overview

A web-based HR management system that centralizes employee information and HR operations while providing a role-aware AI assistant for employees, HR users, and administrators.

Objectives

Centralize employee and HR information.

Manage employees and departments.

Manage attendance, leave, payroll, and performance.

Support onboarding, offboarding, and employee documents.

Provide dashboards, reports, and analytics.

Provide an AI assistant for HR-related queries.

Enforce role-based access to employee information.

Deploy the system using Docker.

User Roles

Administrator

Organization-wide employee and HR management.

Broader database-aware AI queries.

Management of HR modules and reports.

HR

HR operations and employee-related management.

HR assistant functionality.

Employee

Personal employee portal.

Personal attendance, leave, payroll, performance, profile, and related information.

AI access restricted to the employee's own information.

Main Modules

Employee Management

Employees

Employee profiles

Departments

Employee documents

Onboarding

Offboarding

HR Operations

Attendance

Leave management

Payroll

Performance reviews

Reports

Dashboards and analytics

AI and Intelligent Features

AI Assistant

HR Assistant

Database-aware employee queries

Semantic Search

Resume Analyzer

Sentiment Analysis

Local LLM integration

System Architecture

                         Users
                  Admin / HR / Employee
                           |
                           v
                  React + Vite Frontend
                           |
                           | HTTP API
                           v
                    FastAPI Backend
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        HR Services     AI Service    Authentication
             |             |
             |             +------------------+
             |                                |
             v                                v
        PostgreSQL                         Ollama
             |                         TinyLlama Model
             |
             v
      Employee / HR Data

AI Request Flow

User
  |
  v
React AI Assistant
  |
  | POST /ai/chat
  v
FastAPI AI Router
  |
  +--> Authentication / Role Check
  |
  v
AIService
  |
  +--> Employee-specific database queries
  |
  +--> Domain-specific AI logic
  |
  +--> Local LLM when required
              |
              v
           Ollama
              |
              v
      TinyLlama:latest
              |
              v
        AI Response
              |
              v
          Frontend

The AI router authenticates the current user and applies employee access restrictions before passing requests to the AI service.

Employees can access only their own HR information through the AI interface. Administrative users can reach broader database-aware AI processing.

The LLM service uses Ollama with the tinyllama:latest model.

Technology Stack

Frontend

React 19

Vite

Bootstrap 5

React Bootstrap

Axios

Chart.js

React Router

Backend

Python

FastAPI

SQLAlchemy

Pydantic

Database

PostgreSQL 16

AI

Ollama

TinyLlama (tinyllama:latest)

Application-level AI/domain routing

Deployment

Docker

Docker Compose

Nginx

Database Models

The backend contains models for:

User

Employee

Department

Attendance

Leave

Payroll

Performance

Onboarding

Offboarding

Employee Document

Backend Structure

backend/
├── ai/
│   ├── ai_service.py
│   ├── llm_service.py
│   ├── attendance_ai.py
│   ├── leave_ai.py
│   ├── payroll_ai.py
│   ├── performance_ai.py
│   ├── profile_ai.py
│   ├── resume_ai.py
│   ├── semantic_search.py
│   └── sentiment_ai.py
│
├── models/
├── routers/
├── schemas/
└── services/

The backend follows a router/service/model structure, with separate AI components for domain-specific functionality.

Frontend Structure

frontend/src/
├── components/
├── pages/
└── services/

The frontend contains separate employee and administrative/HR pages and service modules for communicating with the backend.

Docker Deployment

The deployed application uses three primary containers:

employee-frontend
    React build served by Nginx
    Port: 5173 -> 80

employee-backend
    FastAPI / Uvicorn
    Port: 8000 -> 8000

employee-postgres
    PostgreSQL 16
    Port: 5432 -> 5432

Docker Compose manages the application services and PostgreSQL volume.

Security

Authentication is applied to AI requests.

User roles are checked before AI processing.

Employees are restricted from requesting other employees' confidential information.

Database-aware AI responses use application data rather than relying only on free-form LLM output.

The local LLM system prompt instructs the assistant not to invent company data.

Database credentials are kept in environment configuration rather than application code.

Current Project Status

Frontend: Working

FastAPI backend: Working

PostgreSQL: Working

Docker deployment: Working

AI Assistant: Working

Role-aware AI restrictions: Implemented

Employee-specific AI queries: Implemented

HR management modules: Implemented

Future Scope

Automated employee account provisioning when HR creates an employee.

Email-based onboarding and password setup.

Stronger authentication and session management.

Advanced RAG over HR policies and company documents.

More comprehensive analytics and dashboards.

Audit logging for sensitive HR and AI operations.

Production HTTPS and domain configuration.

Automated CI/CD deployment.

Architecture Summary

The system is designed as a modular HR platform rather than a standalone chatbot. The core application manages structured employee data through FastAPI and PostgreSQL, while the AI layer provides natural-language access to relevant HR information under role-based security controls.

The AI component combines application-level routing and database logic with a locally hosted Ollama/TinyLlama model, allowing the system to combine structured company data with natural-language assistance.
