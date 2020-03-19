# Create an Argo example from a Boston dataset 

This project is to recreate Argo version from this [code](https://towardsdatascience.com/linear-regression-on-boston-housing-dataset-f409b7e4a155).

## 1. Installation
- Ubuntu 18.04
- Minikube [site](https://kubernetes.io/docs/tasks/tools/install-minikube/)
	- Virtualbox [site](https://www.virtualbox.org/wiki/Linux_Downloads)
- Kubernetes [site](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Argo CLI [site](https://github.com/argoproj/argo/releases)1`
- Docker [site](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

# Step by step
## 1. Start minikube
	$minikube start --driver=virtualbox

## 2. Install other services
- Argo controller, [Step 2 and 3](https://github.com/argoproj/argo/blob/master/docs/getting-started.md)
- MiniIO [Step 5 and 6](https://github.com/argoproj/argo/blob/master/docs/getting-started.md)

## 3. Open URL of the services
### MinIO
	$ minikube service --url argo-artifacts
- AccessKey: AKIAIOSFODNN7EXAMPLE
- SecretKey: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
### Argo UI for version >2.6
	$ sudo kubectl -n argo port-forward deployment/argo-server 27:2746
### Kubernetes dashboard
	$ minikube dashboard

## 4. Test whether your services are running properly

### For Argo
	$ argo submit --watch https://raw.githubusercontent.com/argoproj/argo/master/examples/hello-world.yaml
### For Argo and minIO (non-default)
- Add a my-bucket in your minIO via UI
- Download the output-artifact-s3.yaml
- Add or modified the s3 section

		s3:
			endpoint: argo-artifacts:9000
			insecure: True
			bucket: my-bucket
			key: example/hello_world.txt.tgz
			accessKeySecret:
			name: argo-artifacts
			key: accesskey
			secretKeySecret:
			name: argo-artifacts
			key: secretkey

- Run the yaml file
- If successfully, you should see a file in your minIO

# Get the Boston example running
## 1. File structures
Main directory will have the following
- A list of functions/containers, e.g. 1-CSV-to-df
- The input and output folders, e.g. data and images
- The yaml folder to keep the ARGO yaml files.
- A Dockerize to get the image build
- The example files is the original source from the [website](https://towardsdatascience.com/linear-regression-on-boston-housing-dataset-f409b7e4a155) for ref.

Each modules/container will have the following:
- A docker folder to keep the Dockerfile
- A python source
- A requirement file to keep all the dependency

## 2. To test the python source from local
Download the Boston housing dataset and copy to the data folder

	$ curl -O https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv 
Test each modules from local
	
0. In General

		python3 path/to/source --argument content ...

1. csv-df

		boston$ python3 1-CSV-to-df/CSV_to_df.py --csv_path data/BostonHousing.csv --output_path data/df.pickle
		
		#Output
		This is the name of the script:  1-CSV-to-df/CSV_to_df.py
		Number of arguments:  5
		The arguments are:  ['1-CSV-to-df/CSV_to_df.py', '--csv_path', 'data/BostonHousing.csv', '--output_path', 'data/df.pickle']

2. split-train-test
		
		boston$ python3 2-split-train-test/split_train_test.py --df_path data/df.pickle --list_features lstat rm --target medv --output_path data/split_set.pickle
		
		#Output
		data/df.pickle
		(404, 2)
		(102, 2)
		
3. train-model

		boston$ python3 3-train-model/train_model.py --split_path data/split_set.pickle --output_path data/trained_model.pickle
		
		#Output
		Namespace(output_path='data/trained_model.pickle', split_path='data/split_set.pickle')
		data/split_set.pickle
		The model performance for training set
		--------------------------------------
		RMSE is 5.6371293350711955

4. eval-model

		boston$ python3 4-eval-model/eval_model.py --split_path data/split_set.pickle --trained_model_path data/trained_model.pickle 
		
		#Output
		Namespace(output_path='/tmp/output.pickle', split_path='data/split_set.pickle', trained_model_path='data/trained_model.pickle')
		The model performance for training set
		--------------------------------------
		RMSE is 5.6371293350711955

5. draw-functions - depend on the draw_type different arguments could be selected.

		boston$ python3 2-draw-function/draw_function.py --draw_type hist --df_path data/df.pickle --target medv --save_img_path images/hist.png
		
		boston$ python3 2-draw-function/draw_function.py --draw_type heatmap --df_path data/df.pickle --save_img_path images/heatmap.png`
		
		boston$ python3 2-draw-function/draw_function.py --draw_type plot --df_path data/df.pickle --list_features rm lstat --target medv --save_img_path images/plot.png

## 3. To test the python source from minikube
### 1. Link minikube docker with the local docker repository. ** IMPORTANT you have to do this for each terminal

	$ eval $(minikube docker-env)
	$ docker images

	#Example Output
	
REPOSITORY|TAG|IMAGE ID
|---|---|---
argoproj/workflow-controller|v2.6.3|bdb875f79dfd        
argoproj/argoexec|v2.6.3|594f0cb00d8d 
argoproj/argocli|v2.6.3|195f063d9745
... | ...  | ... 
| k8s.gcr.io/etcd|3.4.3-0|303ce5db0e90

### 2. Dockerize the functions

	$ bash dockerize.sh
	$ docker images

	#Example Output
REPOSITORY|TAG|IMAGE ID
---|---|---
draw-function| 0.0.1| d105e936e8ba 
eval-model |  0.0.1 | 9642679dddaa 
... | ...  | ... 	  
train-model|  0.0.1 | e6af01fd697b  


### 3. Test your images (Optional)

Run your image with --interactive + --tty in docker
	
	$ docker run -it <images> /bin/bash

### 4. Running the Boston example

Add the boston dataset to your minikube via the UI
	
- path: my-bucket/boston/data/
- filename and type: BostonHousing.csv

Run the Argo yaml file
	
	boston$ argo submit yaml/csv-df-train-eval-draw-artifactpassing.yaml
