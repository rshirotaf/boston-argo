echo "*******Building csv-df********"
docker build -f 1-CSV-to-df/docker/Dockerfile -t csv-df .
echo "*******Building Splitting********"
docker build -f 2-split-train-test/docker/Dockerfile -t split-train-test .
echo "*******Building Model********"
docker build -f 3-train-model/docker/Dockerfile -t train-model .
echo "*******Building Eval********"
docker build -f 4-eval-model/docker/Dockerfile -t eval-model .
echo "*******Building Draw Func********"
docker build -f 2-draw-function/docker/Dockerfile -t draw-function .
echo "******* Good Day********"
