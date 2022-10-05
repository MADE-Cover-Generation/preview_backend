import torch


class Normalize(object):
    def __init__(self, mean, var):
        self.mean = mean
        self.var = var

    def __call__(self, sample):
        d_img = sample['d_img_org']
        d_name = sample['d_name']

        d_img = (d_img - self.mean) / self.var

        sample = {'d_img_org': d_img, 'd_name': d_name}
        return sample


class ToTensor(object):
    def __init__(self):
        pass

    def __call__(self, sample):
        d_img = sample['d_img_org']
        d_name = sample['d_name']
        d_img = torch.from_numpy(d_img).type(torch.FloatTensor)
        sample = {
            'd_img_org': d_img,
            'd_name': d_name
        }
        return sample
