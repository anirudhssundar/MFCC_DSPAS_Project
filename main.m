addpath('E:/Scholastic/NITK/Year_3_NITK/Sem-5/Audio Signal Processing/Data/four/')
addpath('E:\Scholastic\NITK\Year_3_NITK\Sem-5\Audio Signal Processing\Data\visual\')
%addpath('E:\Scholastic\NITK\Year_3_NITK\Sem-5\Audio Signal Processing\Data\three\')

files = 'E:\Scholastic\NITK\Year_3_NITK\Sem-5\Audio Signal Processing\Data\visual\';
list = ls(files);


filepath1 = 'visual1.wav';
[mfcc_array1,flag1] = Calc_MFCC(filepath1);

Net = 0;
for i = 5:100
    %filepath1 = list(i,:)
    filepath2 = list(i+1,:)
    
    %filepath2 = 'visual4.wav';
    
    [mfcc_array2,flag2] = Calc_MFCC(strcat(files,filepath2));
    
    
    if((flag1 == 0) | (flag2==0))
        continue
    end
    
    net_dist = 0;
    for i = 1:12
        [distance,d,k,w] = my_dtw(mfcc_array1(:,i),mfcc_array2(:,i));
        net_dist = net_dist+distance;
    end
    net_distance = net_dist/12
    Net = Net + net_distance;

end

Net