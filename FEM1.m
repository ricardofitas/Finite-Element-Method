%% Description

% This is a script to solve numerically a heat transfer problem using the 
% Finite-Element Method

%% Output

% Results of the Ex1

%% Version

%           author: Ricardo Fitas (rfitas99@gmail.com, University of Porto)
%        copyright: 2021 Ricardo Fitas University of Porto
%    creation date: 07/11/2021
%   Matlab version: R2020b
%          Version: 1.0

%% Revision

% V1.0 | 07/11/2021 | Ricardo Fitas | creation

%% Program

clear
close all
clc

%% 1) Variables definition
%% 1.1) Definition of the stiffness, heat coefficient and external forces matrix

syms k I J x P h Ac T_inf T L

funcao = @(x)(k*I*x^(I-1)*J*x^(J-1));
funcao2 = @(x)((P*h*x^I*x^J)/Ac);
funcao3 = @(x)((P*h*(T_inf-T)*x^I)/Ac);

K = int(funcao,0,L);
H = int(funcao2,0,L);
f = int(funcao3,0,L);

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

Dim_ele = 4;

Hloss = NaN(Dim_ele,1);
alfa_mat = NaN(Dim_ele,Dim_ele);

for kk = 1:Dim_ele
    H2 = NaN(kk,kk);
    K2 = NaN(kk,kk);
    f2 = NaN(kk,1);
    xb = cell(kk,1);

    for I = 1:kk
        xb{I,1} = x^I;
        f2(I,1) = subs(f);
        for J = 1:kk
            K2(I,J) = subs(K);
            H2(I,J) = subs(H);
        end
    end

    A = K2 + H2;
    X = A\f2;
    Tx = 0;
    for ii = 1:kk
        Tx = Tx + xb{ii,1}*X(ii,1);
    end
    Tx = Tx + T;
    funcao4 = @(x)(-P*h*(T_inf-Tx));
    syms L1
    func4 = int(funcao4,0,L1);
    L1 = L;
    Hloss(kk,1) = subs(func4);
    for i = 1:kk
        alfa_mat(kk,i) = X(i,1);
    end
end

