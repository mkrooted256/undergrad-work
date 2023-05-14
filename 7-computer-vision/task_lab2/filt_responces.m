%%
H = fftshift(lp_filter('ideal', 500, 500, 50));
mesh(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, 0, 1]);

%%
H = fftshift(lp_filter('btw', 500, 500, 50));
surf(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, 0, 1]);
shading interp;

%%
H = fftshift(lp_filter('gaussian', 500, 500, 50));
surf(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, 0, 1]);
shading interp;

%%
H = fftshift(hp_filter('ideal', 500, 500, 50));
mesh(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, 0, 1]);

%%
H = fftshift(hp_filter('btw', 500, 500, 50));
surf(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, 0, 1]);
shading interp;

%%
H = fftshift(hp_filter('gaussian', 500, 500, 50));
surf(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, 0, 1]);
shading interp;

%%
[U, V] = dftuv(500, 500);
H = -(U .^ 2 + V .^ 2);
surf(H(1:10:500, 1:10:500));
axis([0, 50, 0, 50, -12.5e4, 0]);
shading interp;