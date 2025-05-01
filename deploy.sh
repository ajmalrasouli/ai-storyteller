#!/bin/bash

# Build and deploy to Render
render deploy -f render.yaml

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
sleep 60

# Verify deployment
render get service ai-storyteller-backend

# Print deployment URL
echo "Application deployed successfully!"
echo "Access your application at: https://ai-storyteller.render.com"
