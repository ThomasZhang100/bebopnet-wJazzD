import torch


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name='', fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)# = 5
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True) #ouput is pitch or duration logits but all sequences are concatenated. ,this gets the idx of the 5 largest logits for each prediction, sorted by largest to smallest 
    pred = pred.t().type_as(target) # dim = (5,lengthofconcatenatedsequence)
    correct = pred.eq(target.view(1, -1).expand_as(pred)) #target was (lengthofconcatenatedsequence, 1), now (1, lengthofconcatenatedsequence), expanded to (5, lengthofconcatenatedsequence) target contains the pitch or duration idx of the sequences
    #^^^ gets boolean tensor seeing which of the 5 best predictions are correct for each element
    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size)) #appends the percentage of elements in the batch whose top 3 predictions contain the target
    return res # res = [<percent correct in top 1 precictions>, <percent correct in top 3 precictions>, <percent correct in top 5 precictions>]


def per_class_accuracy(output, target, n_classes):
    """Compute the accuracy per class"""
    batch_size = target.size(0)

    pred = torch.argmax(output, 1)
    pred = pred.unsqueeze(-1).type_as(target)
    pred_expanded = torch.zeros(batch_size, n_classes, device=output.device, dtype=target.dtype).scatter_(1, pred, 1)
    target_expanded = torch.zeros(batch_size, n_classes, device=output.device, dtype=target.dtype).scatter_(1, target,
                                                                                                            1)
    torch.stack((pred_expanded, target_expanded), )
    correct = torch.eq(torch.stack((pred_expanded, target_expanded)).sum(0), 2)

    total_target = target_expanded.sum(0)
    total_target[total_target == 0] = 1
    total_correct = correct.sum(0)

    total_correct = total_correct.float()
    total_target = total_target.float()
    accuracy = total_correct / total_target

    return accuracy
