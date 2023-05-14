function [images, labels] = loadMNIST(path, dataFile, labelsFile, varargin)

    % Read images data
    fileID = fopen(fullfile(path, dataFile), 'rb');
    assert((fileID ~= -1),...
           ['Cannot open file ', fullfile(path, dataFile)]);
    
    magicNumber = fread(fileID, 1, 'uint32', 0, 'b');    % Big-endian
    assert((magicNumber == 2051),...
           'Incorrect MNIST data file: invalid magic number');
      
    imgsNum = fread(fileID, 1, 'uint32', 0, 'b');    % Images number
    imgRows = fread(fileID, 1, 'uint32', 0, 'b');    % Number of rows in each image
    imgCols = fread(fileID, 1, 'uint32', 0, 'b');    % Number of columns in each image
    
    if (~isempty(varargin))    % Read not full base
        number = imgsNum * varargin{1};
        readSize = number * (imgRows * imgCols);
    else                % Read all
        number = imgsNum;
        readSize = inf;
    end
    
    images = fread(fileID, readSize, 'uint8');
    images = reshape(images, imgCols, imgRows, number);
    images = permute(images, [2 1 3]);
    
    fclose(fileID);
    
    % Read labels
    fileID = fopen(fullfile(path, labelsFile), 'rb');
    assert((fileID ~= -1),...
           ['Cannot open file ', fullfile(path, labelsFile)]);
    
    magicNumber = fread(fileID, 1, 'uint32', 0, 'b');	% Big-endian
    assert((magicNumber == 2049),...
           'Incorrect MNIST label file: invalid magic number');
       
    lblsNum = fread(fileID, 1, 'uint32', 0, 'b');       % Labels number
    assert((lblsNum == imgsNum),...
           ['Numbers of images and labels in the specified files ',...
            fullfile(path, dataFile), ' and ', fullfile(path, labelsFile),...
            ' are not equal']);
        
    labels = fread(fileID, number, 'uint8');
    
    fclose(fileID);
end