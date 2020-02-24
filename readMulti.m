%function readMulti(scanset,fileprefix, keepAllResults, showPlots)
set(0,'DefaultFigureWindowStyle','docked')
clc;clear
%%% sync from me to silo - rsync -av /Users/chrisbetters/postdoc-other/rsoft/sweep cbetters@gateway.physics.usyd.edu.au:/import/silo4/snert/FMF_PL_rsoft/
%%% sync from silo to me - rsync -av cbetters@gateway.physics.usyd.edu.au:/import/silo4/snert/FMF_PL_rsoft/sweep /Users/chrisbetters/postdoc-other/rsoft/

%datapath = "/Volumes/silo4/snert/FMF_PL_rsoft/sweep/2_reduced_centre_core/"
%datapath = "/Users/chrisbetters/postdoc-other/rsoft/sweep/4_random_set/"
%datapath = "";
datapath = "S:\sweep\11_atmos_hci_airwrapmodel\"

scanset="hcipysim_"
fileprefix="zernikePSFs"
keepAllResults=false
showPlots=true

matfile=load([datapath + scanset + "_metadata.mat"]);
%matfile=load('PSFOut_hcipy_inputfield.mat');

%%
coeffsList=matfile.coeffsList';
allOutfilenames=matfile.allOutfilenames;
allData=matfile.allData;
% for j=1:size(matfile.allData,1)
%     for i=1:size(matfile.allData,2)
%         allData{j,i}=permute(matfile.allData(j,i,:,:),[3 4 1 2]);
%     end
% end
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
    for i=1:size(allData,1)
            In_psf_ampl(:,:,i) = allData{i,1};
            In_psf_phase(:,:,i) = allData{i,2};
            In_pupil_phase(:,:,i) = allData{i,3};
    end
    %save(datapath+'fldin.mat','InFLDampl','InFLDintens','InFLDphase')
% end

%%
cplot = @(r,x0,y0) plot(x0 + r*cos(linspace(0,2*pi)),y0 + r*sin(linspace(0,2*pi)),'-w');

v = VideoWriter([scanset+'summary'],'MPEG-4');
v.FrameRate=2;
v.Quality=100;
open(v);
figure(1)
for k=1:size(In_psf_ampl,3)
    
    inputFilename = strtrim(allOutfilenames(k,:));
    coeffs = coeffsList(k,:);
    [FLDampl, FLDintens, FLDphase, MONdata(:,:,k), MONposn, XZampl, YZampl] = readall(inputFilename,datapath);
    
    %figure(k);clf
    subplot(3,3,1)
    imagesc([-128 128], [-128 128], (In_psf_ampl(:,:,k).^2))
    hold all
    cplot(55/2,0,0)
    hold off
    title('PSF Intensity')
    
    subplot(3,3,2)
    imagesc([-128 128], [-128 128], In_psf_phase(:,:,k))
    title('PSF Phase')
    
    subplot(3,3,3)
    imagesc(rescale(In_pupil_phase(:,:,k)))
    axis off
    title(['Atmosphere Phase Screen t=' num2str(coeffs)])
    
    subplot(3,3,4)
    imagesc([-250 250], [-250 250], log10(FLDintens))
    xlabel('Simulation Width (um)')
    ylabel('Simulation Height (um)')
    title('PL Output (log10)')
    
    subplot(3,3,5)
    imagesc([0 60], [-250 250], XZampl(:,1:2:end))
    xlabel('Taper Position (mm)')
    ylabel('Simulation Height (um)')
    title('XZ Cut')
    
    subplot(3,3,6)
    imagesc([0 60], [-250 250], YZampl(:,1:2:end))
    xlabel('Taper Position (mm)')
    ylabel('Simulation Width (um)')
    title('YZ Cut')
    
    subplot(3,3,[7:9])
    %plot(MONposn,MONdata)
    title('Core Power Moniters')
    xlabel('Taper Position (mm)')
    ylabel('Power in Core')
    
    MONdata(end,1:7,k)
    sum(MONdata(end,1:7,k))
    %pause
    %%
    frame = getframe(gcf);
    writeVideo(v,frame);
end
close(v);

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

