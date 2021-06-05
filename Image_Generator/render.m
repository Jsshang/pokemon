
window = [];
ModelNum=70;
BackNum=100;

for m = 1:BackNum
   for n = 1:ModelNum
  
[imgModel, map, alpha]  = imread(['E:/毕业设计/模型储存/model/' num2str(n) '.png']); %num2str
[i, j] = find(alpha>0);
iMin = min(i);
iMax = max(i);
jMin = min(j);
jMax = max(j);
alpha = im2uint8(alpha(iMin:iMax, jMin:jMax));
imgModel = im2uint8(imgModel(iMin:iMax, jMin:jMax, :));


imgBG = imread(['E:/毕业设计/模型储存/back/' int2str(m) '.jpg']);
%imgBG = imread('E:/毕业设计/模型储存/background/19.jpg');

sizeBG = size(imgBG);
sizeModel = size(imgModel);

maskBG = zeros(sizeBG(1:2));

k = (rand(1)*0.5)+0.3;


imgModelScale = imresize(imgModel, k);
alphaScale = imresize(alpha, k);

sizeModelScale = size(alphaScale);

xy = ceil(rand(1, 2) .* (sizeBG(1:2)-sizeModelScale));

maskBG(xy(1):xy(1)+sizeModelScale(1)-1, xy(2):xy(2)+sizeModelScale(2)-1) = alphaScale;

imgBG(repmat(maskBG, [1 1 3])>0) =  imgModelScale(repmat(alphaScale, [1 1 3])>0);

%figure;imshow(imgBG)
coord = [((m-1)*ModelNum+n) xy sizeModelScale]; % be careful, x y and row col

window = [window; coord];

%imwrite( imgBG , ['E:/毕业设计/模型储存/result/' num2str(n) '.jpg']);
imwrite( imgBG , ['E:/毕业设计/模型储存/mutiple_trainal/JPEGImages/' num2str((m-1)*ModelNum+n) '.jpg']);
    end
end

%save 'E:/毕业设计/模型储存/flag.txt' window ;

fid=fopen('E:/毕业设计/模型储存/label.txt','A');
[m,n]=size(window);
for i = 1:m 
   if rem(window(i,1),ModelNum)<=10 && rem(window(i,1),ModelNum)>=1
        fprintf(fid,'%.0f.jpg pikachu %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   elseif rem(window(i,1),ModelNum)<=20 && rem(window(i,1),ModelNum)>=1
       fprintf(fid,'%.0f.jpg charizard %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   elseif rem(window(i,1),ModelNum)<=30 && rem(window(i,1),ModelNum)>=1
       fprintf(fid,'%.0f.jpg bulbasaur %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   elseif rem(window(i,1),ModelNum)<=40 && rem(window(i,1),ModelNum)>=1
       fprintf(fid,'%.0f.jpg blastoise %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   elseif rem(window(i,1),ModelNum)<=50 && rem(window(i,1),ModelNum)>=1
       fprintf(fid,'%.0f.jpg eevee %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   elseif rem(window(i,1),ModelNum)<=60 && rem(window(i,1),ModelNum)>=1
       fprintf(fid,'%.0f.jpg lapras %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   else
       fprintf(fid,'%.0f.jpg lucario %.0f %.0f %.0f %.0f\r\n',window(i,1),window(i,3),window(i,2),window(i,3)+window(i,5),window(i,2)+window(i,4));
   end
end


fclose(fid);
%imwirite;