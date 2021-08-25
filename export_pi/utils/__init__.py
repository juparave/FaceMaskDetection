import io
import cv2


def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower():
                return True
    except Exception:
        pass
    return False


def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + \
                (1 - alpha) * src[x + i][y + j]
    return src


def addImageWatermark(LogoImage, MainImage, opacity, pos=(10, 100),):
    opacity = opacity / 100
    OriImg = MainImage
    try:
        waterImg = cv2.imread(LogoImage, -1)
        waterImg = cv2.cvtColor(waterImg, cv2.COLOR_RGBA2BGRA)
    except:
        return OriImg
    tempImg = OriImg.copy()
    print(tempImg.shape)
    overlay = transparentOverlay(tempImg, waterImg, pos)
    output = OriImg.copy()
    # apply the overlay
    cv2.addWeighted(overlay, opacity, output, 1 - opacity, 0, output)

    return output

