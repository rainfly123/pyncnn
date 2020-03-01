import ncnn
from .model_store import get_model_file

class Noop(ncnn.Layer):
    pass

def Noop_layer_creator():
    return Noop()

class MobileNetV2_SSDLite:
    def __init__(self, img_width=300, img_height=300, num_threads=1, use_gpu=False):
        self.img_width = img_width
        self.img_height = img_height
        self.num_threads = num_threads
        self.use_gpu = use_gpu

        self.mean_vals = [127.5, 127.5, 127.5]
        self.norm_vals = [0.007843, 0.007843, 0.007843]

        self.net = ncnn.Net()
        self.net.opt.use_vulkan_compute = self.use_gpu
        #self.net.register_custom_layer("Silence", Noop_layer_creator)
        
        # original pretrained model from https://github.com/chuanqi305/MobileNetv2-SSDLite
        # https://github.com/chuanqi305/MobileNetv2-SSDLite/blob/master/ssdlite/voc/deploy.prototxt
        # the ncnn model https://github.com/caishanli/pyncnn-assets/tree/master/models
        self.net.load_param(get_model_file("mobilenetv2_ssdlite_voc.param"))
        self.net.load_model(get_model_file("mobilenetv2_ssdlite_voc.bin"))

        self.class_names = ["background",
            "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair",
            "cow", "diningtable", "dog", "horse",
            "motorbike", "person", "pottedplant",
            "sheep", "sofa", "train", "tvmonitor"]
            
    def __del__(self):
        self.net = None

    def __call__(self, img):
        img_h = img.shape[0]
        img_w = img.shape[1]

        mat_in = ncnn.Mat.from_pixels_resize(img, ncnn.Mat.PixelType.PIXEL_BGR, img_w, img_h, self.img_width, self.img_height)
        mat_in.substract_mean_normalize(self.mean_vals, self.norm_vals)

        ex = self.net.create_extractor()
        ex.set_light_mode(True)
        ex.set_num_threads(self.num_threads)

        ex.input("data", mat_in)

        mat_out = ncnn.Mat()
        ex.extract("detection_out", mat_out)

        objects = []

        #printf("%d %d %d\n", mat_out.w, mat_out.h, mat_out.c)
        
        #method 1, use ncnn.Mat.row to get the result, no memory copy
        for i in range(mat_out.h):
            values = mat_out.row(i)

            obj = {}
            obj['label'] = values[0]
            obj['prob'] = values[1]
            obj['x'] = values[2] * img_w
            obj['y'] = values[3] * img_h
            obj['w'] = values[4] * img_w - obj['x']
            obj['h'] = values[5] * img_h - obj['y']

            objects.append(obj)
            
        '''
        #method 2, use ncnn.Mat->numpy.array to get the result, no memory copy too
        out = np.array(mat_out)
        for i in range(len(out)):
            values = out[i]
            obj = {}
            obj['label'] = values[0]
            obj['prob'] = values[1]
            obj['x'] = values[2] * img_w
            obj['y'] = values[3] * img_h
            obj['w'] = values[4] * img_w - obj['x']
            obj['h'] = values[5] * img_h - obj['y']
            objects.append(obj)
        '''

        return objects
