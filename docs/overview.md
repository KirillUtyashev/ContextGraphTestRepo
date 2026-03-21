# Overview

This project is a sample backend for a restaurant review website. It is designed to be small enough for class projects, demos, and test repositories while still feeling like a real web backend.

## Purpose

The backend gives a frontend application a simple set of endpoints for:

- listing restaurants
- filtering restaurants by common search criteria
- viewing a single restaurant and its reviews
- creating restaurants
- adding reviews
- loading demo data
- retrieving featured recommendations

## Backend Style

The application uses only the Python standard library. There is no database, ORM, or external web framework. This keeps the repo lightweight and easy to run in environments where the main goal is testing structure, API calls, or collaboration workflows rather than production deployment.

## Core Concepts

### Restaurants

Each restaurant has:

- an auto-generated ID
- a name
- a cuisine
- a location
- a price range
- zero or more reviews

### Reviews

Each review has:

- an auto-generated ID
- an author
- an integer rating from 1 to 5
- a text comment

### Featured Recommendations

The app includes a lightweight recommendation feature that highlights restaurants with stronger ratings and review activity. This logic is separate from the main service so it can be extended independently.

## Runtime Behavior

- Data is stored in memory only
- Server restarts clear all user-created data
- `POST /seed` loads a small sample dataset
- `POST /reset` clears the current in-memory state

## Intended Use

This repo is a good fit for:

- frontend prototypes
- API integration practice
- class or group project demos
- experimenting with backend structure before introducing a framework

If the app later needs authentication, persistence, pagination, or deployment-ready behavior, it would be a good candidate for moving to a framework like FastAPI or Flask and adding a real database.
