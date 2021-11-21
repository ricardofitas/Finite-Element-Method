%% Description

% This is a script to solve numerically a heat transfer problem using the 
% Finite-Element Method (introducing shape functions, using the Heaviside
% function)

%% Output

% Results of the Ex2

%% Version

%           author: Ricardo Fitas (rfitas99@gmail.com, University of Porto)
%        copyright: 2021 Ricardo Fitas University of Porto
%    creation date: 08/11/2021
%   Matlab version: R2020b
%          Version: 1.1

%% Revision

% V1.0 | 07/11/2021 | Ricardo Fitas | creation
% V1.1 | 08/11/2021 | Ricardo Fitas | conclusion of the exercise and
% revision

%% Program

clear
close all
clc

%% 1) Variables definition
%% 1.1) Definition of the stiffness, heat coefficient and external forces matrix

syms k I J x P h Ac T_inf T L

%% 1.2) Constants definition

t = 0.001; % [m]
w = 1; % [m]
L = 0.1; % [m]
k = 360; % [W/(mK)]
h = 9; % [W/(K*m^2)]
T_inf = 20; % [ºC]
T = 235; % [ºC]

P = 2*(w+t);
Ac = w*t;

%% 2) Substitution

Dim_ele = 8;

Hloss = NaN(Dim_ele,1);
alfa_mat = NaN(Dim_ele,Dim_ele+1);

for kk = 1:Dim_ele
    ele_size = L/kk;
    H2 = zeros(kk+1,kk+1);
    K2 = zeros(kk+1,kk+1);
    f2 = zeros(kk+1,1);
    N = cell(1,kk);
    for I = 1:kk
        f2(I:(I+1),1) = f2(I:(I+1),1) + P*h*T_inf*L*[1; 1]/(kk*2*Ac);
        K2(I:(I+1),I:(I+1)) = K2(I:(I+1),I:(I+1)) + k*kk*[1 -1;-1 1]/L;
        H2(I:(I+1),I:(I+1)) = H2(I:(I+1),I:(I+1)) + P*h*L*[2 1;1 2]/(kk*6*Ac);
    end
    A = K2 + H2;
    f2(1,1) = f2(1,1) -A(1,1)*T;
    f2(2,1) = f2(2,1) -A(2,1)*T;
    A(1,1) = -1;
    A(2,1) = 0;
    
    X = A\f2;
    X2 = [T; X(2:end)];
    x1 = x;
    x2 = x-ele_size;
    N0 = heaviside(x1)*heaviside(-x2)*(1-x1/ele_size);
    N1 = heaviside(x1)*heaviside(-x2)*(x1/ele_size);
    Tx = N0*X2(1,1) + N1*X2(2,1);
    for i = 2:kk
        x1 = x-(i-1)*ele_size;
        x2 = x-i*ele_size;
        N0 = heaviside(x1)*heaviside(-x2)*(1-x1/ele_size);
        N1 = heaviside(x1)*heaviside(-x2)*(x1/ele_size);
        Tx = Tx + N0*X2(i,1) + N1*X2(i+1,1);
    end
    funcao4 = @(x)(-P*h*(T_inf-Tx));
    syms L1
    func4 = int(funcao4,0,L1);
    L1 = L;
    Hloss(kk,1) = subs(func4);
    for i = 1:kk+1
        alfa_mat(kk,i) = X2(i,1);
    end
    fplot(x,Tx,[0,L])
    hold on
    
end


