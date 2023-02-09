# pip install -r package.txt \

#CUDA_VISIBLE_DEVICES=0 python cal_onehot.py \
#	--imgs '/data/dataset/SUN_RGBD' \
#	--root 'seg_result/' \
#
CUDA_VISIBLE_DEVICES=0 python map_builder.py \

CUDA_VISIBLE_DEVICES=0 python run.py \
