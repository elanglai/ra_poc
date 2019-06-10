
# number of images per class for training
IMG_TRAIN=60

# split into train and val set
TRAIN_DIR=rockwell_5_train
mkdir -p ${TRAIN_DIR}
for i in ./ra_dataset/*; do
    c=`basename $i`
    echo "spliting $c"
    mkdir -p ${TRAIN_DIR}/$c
    for j in `ls $i/*.JPG | shuf | head -n ${IMG_TRAIN}`; do
        cp $j ${TRAIN_DIR}/$c/
    done
done

# generate lst files
CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MX_DIR=/c/Users/arvkumar/Documents/aws/ML/RA/incubator-mxnet-master
python ${MX_DIR}/tools/im2rec.py --list --recursive ra60-train ${TRAIN_DIR}/
python ${MX_DIR}/tools/im2rec.py --list --recursive ra60-val ./ra_dataset/
mv ra60-train_train.lst ra60-train.lst
rm ra60-train_*
mv ra60-val_train.lst ra60-val.lst
rm ra60-val_*

# generate rec files
python ${MX_DIR}/tools/im2rec.py --resize 256 --quality 95 --num-thread 16 ra60-val ./ra_dataset/
python ${MX_DIR}/tools/im2rec.py --resize 256 --quality 95 --num-thread 16 ra60-train ${TRAIN_DIR}/

