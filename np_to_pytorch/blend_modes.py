import torch

"""
    soft light pytorch implementation
    takes 2 tensors of shape (H,W,3), in range (0.,255.), opacity in range (0.,1.)
    returns a single tensor of shape (H,W,3), in range (0.,255.)
    unlike numpy version, doesn't support alpha channel
"""

def soft_light_pt(img_in, img_layer, opacity, clamp=False):
    img_in_norm = img_in / 255.0
    img_layer_norm = img_layer / 255.0

    ratio = torch.ones_like(img_in[...,0])*opacity

    comp = (1.0 - img_in_norm) * img_in_norm * img_layer_norm \
           + img_in_norm * (1.0 - (1.0 - img_in_norm) * (1.0 - img_layer_norm))

    ratio_rs = torch.reshape(ratio.repeat(1,1,3), [comp.shape[0], comp.shape[1], comp.shape[2]])
    img_out = comp * ratio_rs + img_in_norm * (1.0 - ratio_rs)
    if clamp: img_out = img_out.clamp(0,1)
    return img_out * 255.0

#numpy original source
#https://github.com/flrs/blend_modes/blob/master/blend_modes/blending_functions.py

def soft_light(img_in, img_layer, opacity, disable_type_checks: bool = False):
    """Apply soft light blending mode of a layer on an image.
    Example:
        .. image:: ../tests/soft_light.png
            :width: 30%
        ::
            import cv2, numpy
            from blend_modes import soft_light
            img_in = cv2.imread('./orig.png', -1).astype(float)
            img_layer = cv2.imread('./layer.png', -1).astype(float)
            img_out = soft_light(img_in,img_layer,0.5)
            cv2.imshow('window', img_out.astype(numpy.uint8))
            cv2.waitKey()
    See Also:
        Find more information on
        `Wikipedia <https://en.wikipedia.org/w/index.php?title=Blend_modes&oldid=747749280#Soft_Light>`__.
    Args:
      img_in(3-dimensional numpy array of floats (r/g/b/a) in range 0-255.0): Image to be blended upon
      img_layer(3-dimensional numpy array of floats (r/g/b/a) in range 0.0-255.0): Layer to be blended with image
      opacity(float): Desired opacity of layer for blending
      disable_type_checks(bool): Whether type checks within the function should be disabled. Disabling the checks may
        yield a slight performance improvement, but comes at the cost of user experience. If you are certain that
        you are passing in the right arguments, you may set this argument to 'True'. Defaults to 'False'.
    Returns:
      3-dimensional numpy array of floats (r/g/b/a) in range 0.0-255.0: Blended image
    """

    if not disable_type_checks:
        _fcn_name = 'soft_light'
        assert_image_format(img_in, _fcn_name, 'img_in')
        assert_image_format(img_layer, _fcn_name, 'img_layer')
        assert_opacity(opacity, _fcn_name)

    img_in_norm = img_in / 255.0
    img_layer_norm = img_layer / 255.0

    ratio = _compose_alpha(img_in_norm, img_layer_norm, opacity)

    # The following code does this:
    #   multiply = img_in_norm[:, :, :3]*img_layer[:, :, :3]
    #   screen = 1.0 - (1.0-img_in_norm[:, :, :3])*(1.0-img_layer[:, :, :3])
    #   comp = (1.0 - img_in_norm[:, :, :3]) * multiply + img_in_norm[:, :, :3] * screen
    #   ratio_rs = np.reshape(np.repeat(ratio,3),comp.shape)
    #   img_out = comp*ratio_rs + img_in_norm[:, :, :3] * (1.0-ratio_rs)

    comp = (1.0 - img_in_norm[:, :, :3]) * img_in_norm[:, :, :3] * img_layer_norm[:, :, :3] \
           + img_in_norm[:, :, :3] * (1.0 - (1.0 - img_in_norm[:, :, :3]) * (1.0 - img_layer_norm[:, :, :3]))

    ratio_rs = np.reshape(np.repeat(ratio, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
    img_out = comp * ratio_rs + img_in_norm[:, :, :3] * (1.0 - ratio_rs)
    img_out = np.nan_to_num(np.dstack((img_out, img_in_norm[:, :, 3])))  # add alpha channel and replace nans
    return img_out * 255.0

