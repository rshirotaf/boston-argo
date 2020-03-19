# Argo Yaml

This project is to recreate Argo version from this [code](https://towardsdatascience.com/linear-regression-on-boston-housing-dataset-f409b7e4a155). This section of the code contains the Argo configuration.

To run the main program, you must install and setup following the instruction at the previous page.

    boston$ argo submit yaml/csv-df-train-eval-draw-artifactpassing.yaml

## sample-csv-df-s3.yaml
This setting demonstrate the use of S3 in retrieving and storing of data.

    - name: csv-df-s3-boston
        ...
        artifacts:
        - name: data-CSV
            
            #From docker, the path to save the file
            path: /S3data
            
            s3:
            endpoint: argo-artifacts:9000 
            
            #For the current example this is needed
            insecure: true
            
            #From MinIO, the drive/disk name 
            bucket: my-bucket 
            
            #From MinIO, the path to retrieve the csv
            key: boston/data 
            ...
        container:
        image: csv-df:latest
        imagePullPolicy: Never
        ...

        outputs:
        artifacts:
        - name: data-df
            #From docker, the path to the file
            path: /S3data/df.pickle
            s3:
            ...
            #From MinIO, the path to save the file
            key: boston/data/df.pickle
            ...

## Sample from sample-csv-df-split-artifact-passing
This setting demonstrate the use of artifact passing. For this example, the csv-df passes the df.pickle to split-set.
    
    apiVersion: argoproj.io/v1alpha1
    kind: Workflow
    ...
    templates:
    - name: csv-df-s3-DAG
        dag:
        tasks:
        - name: csv-df
            ...
        - name: split-set
            ...
            arguments:
            #import artifact from other task, e.g. csv-df
            artifacts:
            - name: data-df
                from: "{{tasks.csv-df.outputs.artifacts.data-df}}"
            ...
    - name: split-set-s3-boston
        inputs:
        ...
        #Set the location/filename for the imported file
        artifacts:
        - name: data-df
            path: /S3data/df.pickle
        container:
        ...
        outputs:
        artifacts:
        ...
