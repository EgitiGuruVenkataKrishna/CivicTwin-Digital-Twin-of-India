import torch

def heat_diffusion_residual(T, x, y, t, alpha=0.01):
    """
    Computes PDE residual for heat diffusion: dT/dt - alpha * (d2T/dx2 + d2T/dy2)
    """
    # Gradients w.r.t t
    dT_dt = torch.autograd.grad(T, t, grad_outputs=torch.ones_like(T), create_graph=True, retain_graph=True)[0]
    
    # Gradients w.r.t x
    dT_dx = torch.autograd.grad(T, x, grad_outputs=torch.ones_like(T), create_graph=True, retain_graph=True)[0]
    d2T_dx2 = torch.autograd.grad(dT_dx, x, grad_outputs=torch.ones_like(dT_dx), create_graph=True, retain_graph=True)[0]
    
    # Gradients w.r.t y
    dT_dy = torch.autograd.grad(T, y, grad_outputs=torch.ones_like(T), create_graph=True, retain_graph=True)[0]
    d2T_dy2 = torch.autograd.grad(dT_dy, y, grad_outputs=torch.ones_like(dT_dy), create_graph=True, retain_graph=True)[0]
    
    residual = dT_dt - alpha * (d2T_dx2 + d2T_dy2)
    return residual

def composite_loss(mse_loss, pde_loss, lambda_weight=0.1):
    """
    Combines Data MSE Loss with Physics-Informed PDE loss
    """
    return mse_loss + lambda_weight * pde_loss
