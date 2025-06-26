#!/bin/bash

# 1. 目标头像尺寸（可根据需要修改）
CROP_SIZE=500   # 裁剪区域为500x500像素
RESIZE_SIZE=256 # 最终缩放为256x256像素

# 2. 输入输出目录
INPUT_DIR="driver_photo"
OUTPUT_DIR="driver_avatar"

# 3. 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 4. 批量处理
for file in "$INPUT_DIR"/*.avif; do
  name=$(basename "$file" .avif)
  # 裁剪图片上方CROP_SIZE x CROP_SIZE区域，缩放为RESIZE_SIZE x RESIZE_SIZE
  magick "$file" -gravity north -crop ${CROP_SIZE}x${CROP_SIZE}+0+0 +repage -resize ${RESIZE_SIZE}x${RESIZE_SIZE} "$OUTPUT_DIR/${name}.png"
  echo "裁剪完成: $OUTPUT_DIR/${name}.png"
done

echo "全部裁剪完成！"
