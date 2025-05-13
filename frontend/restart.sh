#!/bin/bash
# Script to reinstall dependencies and restart the frontend development server

echo "Removing node_modules..."
rm -rf node_modules

echo "Cleaning npm cache..."
npm cache clean --force

echo "Installing dependencies..."
npm install

echo "Starting development server..."
npm run serve 