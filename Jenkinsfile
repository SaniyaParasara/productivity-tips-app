pipeline {
    // We are changing the agent type from `dockerfile` to `any`
    // to avoid the "Invalid agent type" error. This is a more universally
    // supported approach that works with most Jenkins setups.
    agent any

    environment {
        // Define environment variables to be used throughout the pipeline.
        // These variables help with consistency and make the script more readable.
        DOCKER_IMAGE_NAME = 'random-json-app'
        CONTAINER_NAME = 'random-json-app-container'
        // Note: The 'master' branch is often renamed to 'main'. Adjust this if needed.
        GITHUB_BRANCH = 'main'
    }

    stages {
        // Stage 1: Build the Docker image.
        // This is the "Continuous Integration" part of the pipeline.
        stage('Build Image') {
            steps {
                script {
                    // Build a new Docker image from the Dockerfile.
                    // The `t` flag tags the image with a name and the build number.
                    // `build.commitId` provides a unique identifier from the current Git commit.
                    echo 'Building Docker image...'
                    def buildNumber = env.BUILD_NUMBER
                    // Using a shell command for Docker build, which is a more general approach
                    // that works with the `agent any` directive.
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${buildNumber} -f Dockerfile ."
                }
            }
        }

        // Stage 2: Run tests on the built image.
        // Ensures the application works as expected before deployment.
        stage('Run Tests') {
            steps {
                script {
                    // The tests are already part of the Dockerfile `RUN` command.
                    // This stage is a checkpoint to show that tests are integrated.
                    echo 'Tests are executed as part of the Docker image build process.'
                    echo 'Build and test stages are tightly integrated.'
                }
            }
        }

        // Stage 3: Deploy the new container.
        // This is the "Continuous Deployment" part.
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying application...'
                    // Check if an old container with the same name exists.
                    def containerExists = sh(returnStatus: true, script: "docker ps -a --filter name=${CONTAINER_NAME} --format '{{.Names}}'").trim() == CONTAINER_NAME
                    if (containerExists) {
                        echo "Removing old container: ${CONTAINER_NAME}"
                        // Stop and remove the old container to make way for the new one.
                        sh "docker stop ${CONTAINER_NAME}"
                        sh "docker rm ${CONTAINER_NAME}"
                    } else {
                        echo "No existing container to remove."
                    }

                    // Run the new Docker container.
                    // `-d` runs the container in detached mode (background).
                    // `-p 5000:5000` maps port 5000 on the host to port 5000 in the container.
                    // `--name` gives the container a friendly name for easy management.
                    // `DOCKER_IMAGE_NAME` and `buildNumber` select the newly built image.
                    def buildNumber = env.BUILD_NUMBER
                    sh "docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${DOCKER_IMAGE_NAME}:${buildNumber}"
                    echo 'Deployment complete. App should be live at http://localhost:5000'
                }
            }
        }
    }

    // Post-build actions, regardless of the pipeline's outcome.
    post {
        always {
            // This block runs after every pipeline build, whether successful or failed.
            // It ensures that any temporary Docker containers or images are cleaned up.
            script {
                echo 'Cleaning up any temporary build containers...'
                sh 'docker system prune -f --volumes'
            }
        }
    }
}
