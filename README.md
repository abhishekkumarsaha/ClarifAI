# ClarifAI

AI-Assisted News Verification Platform

## Live Demo

Frontend:
https://clarifai-frontend20.vercel.app

## Overview

ClarifAI is an AI-assisted news verification platform designed to help users evaluate news claims by combining live news retrieval, evidence analysis, source evaluation, and AI-generated explanations.

## Features

- News claim verification
- AI-assisted analysis
- Live news retrieval
- Evidence-based results
- Source ranking
- Verification verdicts
- Verification history
- Responsive web interface
- FastAPI backend
- React + TypeScript frontend

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- Framer Motion

### Backend
- Python
- FastAPI
- Uvicorn

### AI / Data
- OpenRouter
- Currents API
- Source ranking
- Evidence pipeline

### Deployment
- Vercel

## Architecture

React Frontend
       ↓
FastAPI API
       ↓
News Retrieval
       ↓
Evidence Pipeline
       ↓
Source Ranking
       ↓
AI Analysis
       ↓
Verification Result

## API

GET /api
GET /api/health
GET /api/news
POST /api/analyze
POST /api/verify

## Local Development

### Backend

Create and activate a Python virtual environment and install:

pip install -r requirements.txt

Run:

uvicorn api.index:app --reload

### Frontend

cd frontend

npm install

npm run dev

## Environment Variables

Frontend:

VITE_API_BASE_URL

Backend:

CURRENTS_API_KEY
OPENROUTER_API_KEY
OPENROUTER_MODEL
FRONTEND_URL

## Deployment

Frontend and backend are deployed using Vercel.

## Project Structure

ClarifAI/
├── api/
├── src/
├── frontend/
├── data/
├── requirements.txt
└── README.md

## Future Improvements

- More verification sources
- Improved evidence aggregation
- Enhanced source credibility scoring
- Better historical verification analytics
- Additional AI models
- Expanded multilingual support

## Author

A.K. Abhishek Kumar Saha
