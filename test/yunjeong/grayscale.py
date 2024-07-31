import cv2
import numpy as np

# 원본 이미지 읽기
img = cv2.imread('image_path', cv2.IMREAD_COLOR)

# 이진화를 적용할 영역 좌표 (x0, y0)부터 (x1, y1)까지
x0, y0 = 200, 200
x1, y1 = 500, 500

# 해당 영역의 이미지 추출
roi = img[y0:y1, x0:x1]

# # 그레이스케일 변환
# gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# # 이진화 적용 (임계값 127, 최대값 255)
# _, binary_roi = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)

# # 이진화된 부분을 컬러 이미지로 변환
# binary_roi_color = cv2.cvtColor(binary_roi, cv2.COLOR_GRAY2BGR)

# # 원본 이미지에 이진화된 부분 삽입
# img[y0:y1, x0:x1] = binary_roi_color

# # 결과 이미지 저장 또는 표시
# # cv2.imwrite('binary_image.jpg', img)
# cv2.imshow('gray',gray_roi)
# cv2.imshow('original' , img)

# cv2.waitKey(0)


# # 그레이스케일 변환
# gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# 이진화 적용 (임계값 127, 최대값 255)
_, binary_roi = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)

# # 이진화된 부분을 컬러 이미지로 변환
# binary_roi_color = cv2.cvtColor(binary_roi, cv2.COLOR_GRAY2BGR)

# 원본 이미지에 이진화된 부분 삽입
img[y0:y1, x0:x1] = binary_roi

# 결과 이미지 저장 또는 표시
# cv2.imwrite('binary_image.jpg', img)
# cv2.imshow('gray',gray_roi)
cv2.imshow('original' , img)
cv2.imshow('binary_roi' , binary_roi)

cv2.waitKey(0)