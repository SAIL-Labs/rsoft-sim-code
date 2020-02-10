%function readMulti(scanset,fileprefix, keepAllResults, showPlots)
set(0,'DefaultFigureWindowStyle','docked')
%%% sync from me to silo - rsync -av /Users/chrisbetters/postdoc-other/rsoft/sweep cbetters@gateway.physics.usyd.edu.au:/import/silo4/snert/FMF_PL_rsoft/
%%% sync from silo to me - rsync -av cbetters@gateway.physics.usyd.edu.au:/import/silo4/snert/FMF_PL_rsoft/sweep /Users/chrisbetters/postdoc-other/rsoft/

%datapath = "/Volumes/silo4/snert/FMF_PL_rsoft/sweep/2_reduced_centre_core/"
datapath = "/Users/chrisbetters/postdoc-other/rsoft/sweep/4_random_set/"

scanset="randset_"
fileprefix="zernikePSFs"
keepAllResults=false
showPlots=true

load([datapath + scanset + "_metadata.mat"])
%% 
% try
%     load('fldin.mat','InFLDampl','InFLDintens','InFLDphase')
% 
% catch
%     for i=1:size(coeffsList,2)
%         [InFLDampl(:,:,i), InFLDintens(:,:,i), InFLDphase(:,:,i)] = loadInputFLD(fileprefix+'_'+sprintf('%.1f_',coeffsList(:,i))+'inputfield',datapath);
%     end
%     save('fldin.mat','InFLDampl','InFLDintens','InFLDphase')
% end
% catch
    for i=1:size(coeffsList,1)
            In_psf_ampl(:,:,i) = allData{i,1};
            In_psf_phase(:,:,i) = allData{i,2};
            In_pupil_phase(:,:,i) = allData{i,3};
    end
    %save(datapath+'fldin.mat','InFLDampl','InFLDintens','InFLDphase')
% end

%%

for k=1:size(allOutfilenames,1)
    
    inputFilename = allOutfilenames(k,:);
    coeffs = coeffsList(k,:);
    [FLDampl, FLDintens, FLDphase, MONdata, MONposn, XZampl, YZampl] = readall(inputFilename,datapath);
    
    figure(k+3)
    subplot(3,3,1)
    imagesc((In_psf_ampl(:,:,k).^2))
    
    subplot(3,3,2)
    imagesc(In_psf_phase(:,:,k))
    
    subplot(3,3,3)
    imagesc(In_pupil_phase(:,:,k))
    
    subplot(3,3,4)
    imagesc((FLDintens))
    
    subplot(3,3,5)
    imagesc(XZampl(:,1:2:end))
    
    subplot(3,3,6)
    imagesc(YZampl(:,1:2:end))
    
    subplot(3,3,[7:9])
    plot(MONposn,MONdata)
    
    MONdata(end,1:7)
    sum(MONdata(end,1:7))
    %pause
end

%% Cubes
for k=1:size(allOutfilenames,1)
    inputFilename = allOutfilenames(k,:);
    Acube=loadCube(inputFilename,datapath);
    Acube=Acube(:,1:end-1,:);
    
    cmap = parula(256);
    sliceViewer(Acube,'Colormap',cmap)  
end

%% Functions
function [FLDampl, FLDintens, FLDphase, MONdata, MONposn, XZampl, YZampl] = readall(inputFilename,datapath)
    try
        load([datapath + inputFilename + '.mat'],'FLDampl', 'FLDintens', 'FLDphase', 'MONdata', 'MONposn', 'XZampl', 'YZampl')
    catch
        [FLDampl, FLDintens, FLDphase] = loadFLD(inputFilename,datapath);
        [MONdata, MONposn] = loadMON(inputFilename,datapath);
        [XZampl] = loadXZ(inputFilename, datapath);
        [YZampl] = loadYZ(inputFilename, datapath);
        save([datapath + inputFilename + '.mat'],'FLDampl', 'FLDintens', 'FLDphase', 'MONdata', 'MONposn', 'XZampl', 'YZampl')
    end
end

function [FLDampl, FLDintens, FLDphase] = loadFLD(filename,datapath)
    A = readmatrix(datapath + filename + ".fld",'NumHeaderLines',4,'FileType','text');
    FLDampl = A(:,1:2:end-1);
    FLDintens = A(:,1:2:end-1).^2;
    FLDphase = A(:,2:2:end);
end

function [MONdata, MONposn] = loadMON(filename,datapath)
    A = readmatrix(datapath + filename + ".mon",'NumHeaderLines',5,'FileType','text');
    MONdata = A(:,2:end);
    MONposn = A(:,1);
end

function [XZampl] = loadXZ(filename, datapath)
    XZampl = readmatrix(datapath + filename + "_xz.dat",'NumHeaderLines',4,'FileType','text');    
end

function [YZampl] = loadYZ(filename, datapath)
    YZampl = readmatrix(datapath + filename + "_yz.dat",'NumHeaderLines',4,'FileType','text');    
end

function [FLDampl, FLDintens, FLDphase] = loadInputFLD(filename,datapath)
    
    A = readmatrix(datapath + filename + ".fld",'NumHeaderLines',4,'FileType','text');
    FLDampl = A(:,1:2:end-1);
    FLDintens = A(:,1:2:end-1).^2;
    FLDphase = A(:,2:2:end);
end

function Acube=loadCube(filename,datapath)
    try
        load([datapath + filename + '_cube.mat'],'Acube')
    catch
        
        filenames=dirFilenames(datapath+filename+'*','\.[0-9]+$');
        for i=1:length(filenames)
            Acube(:,:,i) = readmatrix(datapath + filenames{i} ,'NumHeaderLines',4,'FileType','text');
        end
        save([datapath + filename + '_cube.mat'],'Acube')
    end
end

