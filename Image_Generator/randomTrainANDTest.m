xmlfilepath='E:mutiple_trainal\Annotations';  
txtsavepath='E:mutiple_trainal\ImageSets\Main\';  
trainval_percent=0.6;
train_percent=0.6;
  
xmlfile=dir(xmlfilepath);  
numOfxml=length(xmlfile)-2;
  
  
trainval=sort(randperm(numOfxml,floor(numOfxml*trainval_percent)));  
test=sort(setdiff(1:numOfxml,trainval));  
  
  
trainvalsize=length(trainval);
train=sort(trainval(randperm(trainvalsize,floor(trainvalsize*train_percent))));  
val=sort(setdiff(trainval,train));  
  
  
ftrainval=fopen([txtsavepath 'trainval.txt'],'w');  
ftest=fopen([txtsavepath 'test.txt'],'w');  
ftrain=fopen([txtsavepath 'train.txt'],'w');  
fval=fopen([txtsavepath 'val.txt'],'w');  
  
  
for i=1:numOfxml  
    if ismember(i,trainval)  
        fprintf(ftrainval,'%s\r\n',xmlfile(i+2).name(1:end-4));  
        if ismember(i,train)  
            fprintf(ftrain,'%s\r\n',xmlfile(i+2).name(1:end-4));  
        else  
            fprintf(fval,'%s\r\n',xmlfile(i+2).name(1:end-4));  
        end  
    else  
        fprintf(ftest,'%s\r\n',xmlfile(i+2).name(1:end-4));  
    end  
end  
fclose(ftrainval);  
fclose(ftrain);  
fclose(fval);  
fclose(ftest);  
