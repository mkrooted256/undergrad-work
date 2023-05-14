function [VG, A, PPG] = colorgrad(F, T)
    %COLORGRAD Computes the vector gradient of an RGB image.
    % [VG, VA, PPG] = colorgrad(F, T) computes the vector gradient, VG, and 
    % corresponding angle array, A, (in radians) of RGB image F. It also 
    % computes PPG, the per-plane composite gradient obtained by summing 
    % the 2-D gradients of the individual color planes. Input T is a 
    % threshold in the range [0, 1]. If it is included in the argument list, 
    % the values of VG and PPG are thresholded by letting VG(x,y) = 0 for 
    % values <= T and VG(x,y) = VG(x,y) otherwise. Similar comments apply 
    % to PPG. If T is not included in the argument list then T is set to 0.
    %  Both output gradients are scaled to the range [0, 1]. 

    if (ndims(F) ~= 3)
        error('Input image must be RGB');
    end

    % Compute the x and y derivatives of the three component images using
    % Sobel operator 
    h_x = fspecial('sobel');
    h_y = h_x';

    Rx = imfilter(double(F(:, :, 1)), h_x, 'replicate');
    Ry = imfilter(double(F(:, :, 1)), h_y, 'replicate');

    Gx = imfilter(double(F(:, :, 2)), h_x, 'replicate');
    Gy = imfilter(double(F(:, :, 2)), h_y, 'replicate');

    Bx = imfilter(double(F(:, :, 3)), h_x, 'replicate');
    By = imfilter(double(F(:, :, 3)), h_y, 'replicate');

    % Compute the parameters of the vector gradient (VG).
    gxx = Rx .^ 2 + Gx .^ 2 + Bx .^ 2;
    gyy = Ry .^ 2 + Gy .^ 2 + By .^ 2;
    gxy = Rx .* Ry + Gx .* Gy + Bx .* By;

    A = 0.5 * (atan((2*gxy) ./ (gxx - gyy + eps)));
    G1 = 0.5 * ((gxx + gyy) + (gxx - gyy) .* cos (2*A) + 2 * gxy .* sin (2*A));

    A = A + pi / 2; % Now repeat for angle + pi / 2
    G2 = 0.5 * ((gxx + gyy) + (gxx - gyy) .* cos (2*A) + 2 * gxy .* sin (2*A));

    G1 = sqrt(G1);
    G2 = sqrt(G2);
    % Picking the maximum at each (x, y) and then scale to range [0, 1].
    VG = mat2gray(max(G1, G2));

    % Compute per-plane gradients.
    RG = sqrt(Rx .^ 2 + Ry .^ 2);
    GG = sqrt(Gx .^ 2 + Gy .^ 2);
    BG = sqrt(Bx .^ 2 + By .^ 2);

    % Composite gradient image scaled to [0, 1].
    PPG = mat2gray(RG + GG + BG);

    % Threshold the result
    if (nargin == 2)
        VG = (VG > T) .* VG;
        PPG = (PPG > T) .* PPG;
    end
end

