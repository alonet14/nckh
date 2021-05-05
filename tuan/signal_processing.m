clear all

% Lay du lieu tu file excel
data = xlsread('rate-100-NofS-100-60s','sheet1','B2:B6101');

% Thoi gian do
ts = 60;

% Chuyen doi sang truc thoi gian
size_data = size(data);
t = [1:size_data(:,1)]*ts/size_data(:,1);

% Dau vao bo loc
fs=100;
fL=0.83;
fH=2.33;
fr = 0.5;

% Loc tin hieu nhip tim
[b,a] = butter(3,[fL/(fs/2) fH/(fs/2)]); % Lay tham so cua bo loc thong dai
HR = filter(b,a,data); % Loc tin hieu voi bo tham so a, b duoc tra ve
threshold_HR = (max(HR)-min(HR))*0.01; % Muc nguong
[pkh,lch] = findpeaks(HR,t, 'MinPeakDistance', 0.5, 'MinPeakHeight', threshold_HR); % Ham tim dinh, tra ve bo gia tri dinh va vi tri
HR_size = size(pkh);
NofHR = HR_size(:,1); % So luong dinh
%interval_hr = interval_data(lch);
interval_hr = diff(lch); % Vector thoi gian giua cac dinh
sdhi = std(interval_hr); % Tinh SDHI
fprintf('Heart rate: %d\n', int8((NofHR/ts)*60)); 
fprintf('SDHI: %d\n', sdhi);

% Loc tin hieu nhip tho
[d,c] = butter(5,fr/(fs/2)); % Lay tham so cua bo loc thong thap
RR = filter(d,c,data); % Loc tin hieu voi bo tham so c, d duoc tra ve
threshold_RR = (max(RR)-min(RR))*0.01; % Muc nguong
[pkr,lcr] = findpeaks(RR, t, 'MinPeakDistance', 2.5, 'MinPeakHeight',threshold_RR); % Ham tim dinh, tra ve bo gia tri dinh va vi tri
%interval_rr = diff(lcr);
%RR_size = size(pkr);
NofRR = RR_size(:,1);
fprintf('Respiratory rate: %d\n', int8((NofRR/ts)*60));

% Ve do thi tin hieu goc
figure(1);
plot(t, data);
xlabel('Time');
ylabel('Intensity');
title('Original Signal');

% Ve do thi nhip tim va danh dau dinh
figure(2);
plot(t, HR);
xlabel('Time');
ylabel('Intensity');
title('Heart Signal');
hold on;
%text(lch,pkh,num2str((1:numel(pkh))'))
plot(lch,pkh,'x');

% Ve do thi nhip tho va danh dau dinh
figure(3);
plot(t, RR);
xlabel('Time');
ylabel('Intensity');
title('Respiratory Signal');
hold on;
%text(lcr,pkr,num2str((1:numel(pkr))'))
plot(lcr,pkr,'x');
