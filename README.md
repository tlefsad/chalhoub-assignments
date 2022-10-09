# Task 1 - Programming with Python Context
- Please review the documentation for the Github API. We want to be able to process and analyze pull requests information for different Github repositories. Your goal is to prepare a data pipeline that will read the pull requests for the provided repositories and load them into a BigQuery for a further analysis. You can also pick any database or any other output format of your choice as well (in this case, please describe the advantages of your choice and make sure it is convenient for the downstream processing and analysis).


## Tech Details and Requirements
- In order to build the pipeline in Google Cloud environment, create a free GCP project to complete this case study(if this is not possible please reach out to us so we can create a sandbox instance for you).
- Prepare a pipeline implemented with Python programming language to read the pull-requests for the provided Github repositories every day and load them into the BigQuery table.
- Load historical data for the last 30 days if it is possible.
- Remember to clean up the data if necessary.
- There should be information on how we can make it run (what do we need to install? How do we execute the pipeline?).
- The code should be well documented.
- How would you test and deploy further changes in the code?
- What would be the best way to monitor the performance of the pipeline?


### How to Run

1. Prepare GCP development environment. 
        https://cloud.google.com/functions/docs/create-deploy-gcloud
2. Acquire Github access token 
        https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
3. Define `.env.yaml` as following.
   ```yaml
    GITHUB_ACCESS_TOKEN: your-token
    GCP_PROJECT_ID: your-project
    GCP_TABLE_ID: your-project.your_dataset.your_table_name
    ```
4. Deploy Google Cloud Function (Gen 2)
   ```shell
    gcloud functions deploy ${your-function-name} \
        --gen2 \
        --trigger-http \
        --entry-point fetch_pull_requests \
        --region ${your-region} \
        --runtime python310 \
        --timeout 600 \
        --env-vars-file .env.yaml \
        --service-account ${your-service-account}
   ```
5. Create Google Cloud Scheduler

   ```shell
    gcloud scheduler jobs create http ${your-job-name} \
        --location ${your-location} \
        --schedule ${schedule} \
        --uri ${your-gcf-uri} \
        --headers "Content-Type=application/json" \
        --message-body ${your-message-body} \
        --http-method POST
   ```
    Example of `--message-body`
    ```shell
      --message-body '{"repositories": "PyGithub/PyGithub,torvalds/linux"}'
    ```
    name of repositories delimited by comma
