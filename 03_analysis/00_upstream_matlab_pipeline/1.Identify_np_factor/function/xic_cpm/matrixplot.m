function matrixplot(data,varargin)
%   æ ¹æ®å®å¼ç©éµç»å¶è²åå¾ï¼ç¨ä¸°å¯çé¢è²åå½¢ç¶å½¢è±¡çå±ç¤ºç©éµåç´ å¼çå¤§å°ã
%
%   matrixplot(data) ç»å¶ç©éµè²åå¾ï¼dataä¸ºå®å¼ç©éµï¼æ¯ä¸ä¸ªåç´ å¯¹åºä¸ä¸ªè²åï¼è²
%                    åé¢è²ç±åç´ å¼å¤§å°å³å®ã
%
%   matrixplot(data, 'PARAM1',val1, 'PARAM2',val2, ...) 
%          ç¨æå¯¹åºç°çåæ°å/åæ°å¼æ§å¶è²åçåé¡¹å±æ§ãå¯ç¨çåæ°å/åæ°å¼å¦ä¸ï¼
%          'FigShape' --- è®¾å®è²åçå½¢ç¶ï¼å¶åæ°å¼ä¸ºï¼
%                'Square'  --- æ¹å½¢ï¼é»è®¤ï¼
%                'Circle'  --- åå½¢
%                'Ellipse' --- æ¤­åå½¢
%                'Hexagon' --- å­è¾¹å½¢
%                'Dial'    --- è¡¨çå½¢
%
%          'FigSize' --- è®¾å®è²åçå¤§å°ï¼å¶åæ°å¼ä¸ºï¼
%                'Full'    --- æå¤§è²åï¼é»è®¤ï¼
%                'Auto'    --- æ ¹æ®ç©éµåç´ å¼èªå¨ç¡®å®è²åå¤§å°
%
%          'FigStyle' --- è®¾å®ç©éµå¾æ ·å¼ï¼å¶åæ°å¼ä¸ºï¼
%                'Auto'    --- ç©å½¢ç©éµå¾ï¼é»è®¤ï¼
%                'Tril'    --- ä¸ä¸è§ç©éµå¾
%                'Triu'    --- ä¸ä¸è§ç©éµå¾
%
%          'FillStyle' --- è®¾å®è²åå¡«åæ ·å¼ï¼å¶åæ°å¼ä¸ºï¼
%                'Fill'    --- å¡«åè²ååé¨ï¼é»è®¤ï¼
%                'NoFill'  --- ä¸å¡«åè²ååé¨
%
%          'DisplayOpt' --- è®¾å®æ¯å¦å¨è²åä¸­æ¾ç¤ºç©éµåç´ å¼ï¼å¶åæ°å¼ä¸ºï¼
%                'On'      --- æ¾ç¤ºç©éµåç´ å¼ï¼é»è®¤ï¼
%                'Off'     --- ä¸æ¾ç¤ºç©éµåç´ å¼
%
%          'TextColor' --- è®¾å®æå­çé¢è²ï¼å¶åæ°å¼ä¸ºï¼
%                è¡¨ç¤ºåè²çå­ç¬¦ï¼'r','g','b','y','m','c','w','k'ï¼,é»è®¤ä¸ºé»è²
%                1è¡3åççº¢ãç»¿ãèä¸åè²ç°åº¦å¼åéï¼[r,g,b]ï¼
%                'Auto'    --- æ ¹æ®ç©éµåç´ å¼èªå¨ç¡®å®æå­é¢è²
%
%          'XVarNames' --- è®¾å®Xè½´æ¹åéè¦æ¾ç¤ºçåéåï¼é»è®¤ä¸ºX1,X2,...ï¼ï¼å¶åæ°å¼ä¸ºï¼
%                å­ç¬¦ä¸²ç©éµæå­ç¬¦ä¸²åèæ°ç»ï¼è¥ä¸ºå­ç¬¦ä¸²ç©éµï¼å¶è¡æ°åºä¸dataçåæ°ç¸å
%                è¥ä¸ºå­ç¬¦ä¸²åèæ°ç»ï¼å¶é¿åº¦åºä¸dataçåæ°ç¸åã
%
%          'YVarNames' --- è®¾å®Yè½´æ¹åéè¦æ¾ç¤ºçåéåï¼é»è®¤ä¸ºY1,Y2,...ï¼ï¼å¶åæ°å¼ä¸ºï¼
%                å­ç¬¦ä¸²ç©éµæå­ç¬¦ä¸²åèæ°ç»ï¼è¥ä¸ºå­ç¬¦ä¸²ç©éµï¼å¶è¡æ°åºä¸dataçè¡æ°ç¸å
%                è¥ä¸ºå­ç¬¦ä¸²åèæ°ç»ï¼å¶é¿åº¦åºä¸dataçè¡æ°ç¸åã
%
%          'ColorBar' --- è®¾å®æ¯å¦æ¾ç¤ºé¢è²æ¡ï¼å¶åæ°å¼ä¸ºï¼
%                'On'      --- æ¾ç¤ºé¢è²æ¡
%                'Off'     --- ä¸æ¾ç¤ºé¢è²æ¡ï¼é»è®¤ï¼
%
%          'Grid' --- è®¾å®æ¯å¦æ¾ç¤ºç½æ ¼çº¿ï¼å¶åæ°å¼ä¸ºï¼
%                'On'      --- æ¾ç¤ºç½æ ¼çº¿ï¼é»è®¤ï¼
%                'Off'     --- ä¸æ¾ç¤ºç½æ ¼çº¿
%
%   Example:
%   x = [1,-0.2,0.3,0.8,-0.5
%        -0.2,1,0.6,-0.7,0.2
%         0.3,0.6,1,0.5,-0.3
%         0.8,-0.7,0.5,1,0.7
%        -0.5,0.2,-0.3,0.7,1];
%   matrixplot(x);
%   matrixplot(x,'DisplayOpt','off');
%   matrixplot(x,'FillStyle','nofill','TextColor','Auto');
%   matrixplot(x,'TextColor',[0.7,0.7,0.7],'FigShap','s','FigSize','Auto','ColorBar','on');
%   matrixplot(x,'TextColor','k','FigShap','d','FigSize','Full','ColorBar','on','FigStyle','Triu');
%   XVarNames = {'xiezhh','heping','keda','tust','tianjin'};
%   matrixplot(x,'FigShap','e','FigSize','Auto','ColorBar','on','XVarNames',XVarNames,'YVarNames',XVarNames);
%
%   CopyRightï¼xiezhhï¼è°¢ä¸­åï¼,2013.01.24ç¼å

% å¯¹ç¬¬ä¸ä¸ªè¾å¥åæ°ç±»åè¿è¡å¤æ­
if ~ismatrix(data) || ~isreal(data)
    error('è¾å¥åæ°ç±»åä¸å¹éï¼ç¬¬ä¸ä¸ªè¾å¥åæ°åºä¸ºå®å¼ç©éµ');
end

% è§£ææå¯¹åºç°çåæ°å/åæ°å¼
[FigShape,FigSize,FigStyle,FillStyle,DisplayOpt,TextColor,XVarNames,...
    YVarNames,ColorBar,GridOpt] = parseInputs(varargin{:});

% äº§çç½æ ¼æ°æ®
[m,n] = size(data);
[x,y] = meshgrid(0:n,0:m);
data = data(:);
maxdata = nanmax(data);
mindata = nanmin(data);
rangedata = maxdata - mindata;
if isnan(rangedata)
    warning('MATLAB:warning1','è¯·æ£æ¥æ¨è¾å¥çç©éµæ¯å¦åéï¼');
    return;
end
z = zeros(size(x))+0.2;
sx = x(1:end-1,1:end-1)+0.5;
sy = y(1:end-1,1:end-1)+0.5;

if strncmpi(FigStyle,'Tril',4)
    z(triu(ones(size(z)),2)>0) = NaN;
    sx(triu(ones(size(sx)),1)>0) = NaN;
elseif strncmpi(FigStyle,'Triu',4)
    z(tril(ones(size(z)),-2)>0) = NaN;
    sx(tril(ones(size(sx)),-1)>0) = NaN;
end
sx = sx(:);
sy = sy(:);
id = isnan(sx) | isnan(data);
sx(id) = [];
sy(id) = [];
data(id) = [];

if isempty(XVarNames)
    XVarNames = strcat('X',cellstr(num2str((1:n)')));
else
    if (iscell(XVarNames) && (numel(XVarNames) ~= n)) || (~iscell(XVarNames) && (size(XVarNames,1) ~= n))
        error('Xè½´æ¹ååéååºä¸ºå­ç¬¦ä¸²ç©éµæå­ç¬¦ä¸²åèæ°ç»ï¼å¶é¿åº¦ä¸è¾å¥ç©éµçåæ°ç¸å');
    end
end
if isempty(YVarNames)
    YVarNames = strcat('Y',cellstr(num2str((1:m)')));
else
    if (iscell(YVarNames) && (numel(YVarNames) ~= m)) || (~iscell(YVarNames) && (size(YVarNames,1) ~= m))
        error('Yè½´æ¹ååéååºä¸ºå­ç¬¦ä¸²ç©éµæå­ç¬¦ä¸²åèæ°ç»ï¼å¶é¿åº¦ä¸è¾å¥ç©éµçè¡æ°ç¸å');
    end
end

% ç»å¾
figure('color','w',...
    'units','normalized',...
    'pos',[0.289165,0.154948,0.409956,0.68099]);
axes('units','normalized','pos',[0.1,0.022,0.89,0.85]);
if strncmpi(GridOpt,'On',2)
    mesh(x,y,z,...
        'EdgeColor',[0.7,0.7,0.7],...
        'FaceAlpha',0,...
        'LineWidth',1);   % åèç½æ ¼çº¿
end
hold on;
axis equal;
axis([-0.1,n+0.1,-0.1,m+0.1,-0.5,0.5]);
view(2);
% è®¾ç½®Xè½´åYè½´å»åº¦ä½ç½®åæ ç­¾
set(gca,'Xtick',(1:n)-0.5,...
    'XtickLabel',XVarNames,...
    'Ytick',(1:m)-0.5,...
    'YtickLabel',YVarNames,...
    'XAxisLocation','top',...
    'YDir','reverse',...
    'Xcolor',[0.7,0.7,0.7],...
    'Ycolor',[0.7,0.7,0.7],...
    'TickLength',[0,0],...
    'FontSize',13);
axis off

% ç»å¶å¡«åè²å
if strncmpi(FillStyle,'Fill',3)
    MyPatch(sx',sy',data',FigShape,FigSize);
end

% æ¾ç¤ºæ°å¼ææ¬ä¿¡æ¯
if strncmpi(DisplayOpt,'On',2)
    str = num2str(data,'%4.3f');
    scale = 0.1*max(n/m,1)/(max(m,n)^0.55);
    if strncmpi(TextColor,'Auto',3)
        ColorMat = get(gcf,'ColorMap');
        nc = size(ColorMat,1);
        cid = fix(mapminmax(data',0,1)*nc)+1;
        cid(cid<1) = 1;
        cid(cid>nc) = nc;
        TextColor = ColorMat(cid,:);
        for i = 1:numel(data)
            text(sx(i),sy(i),0.1,str(i,:),...
                'FontUnits','normalized',...
                'FontSize',scale,...
                'fontweight','bold',...
                'HorizontalAlignment','center',...
                'Color',TextColor(i,:));
        end
    else
        text(sx,sy,0.1*ones(size(sx)),str,...
            'FontUnits','normalized',...
            'FontSize',scale,...
            'fontweight','bold',...
            'HorizontalAlignment','center',...
            'Color',TextColor);
    end
end

% è®¾ç½®Xè½´åYè½´å»åº¦æ ç­¾çç¼©è¿æ¹å¼
MyTickLabel(gca,FigStyle);

% æ·»å é¢è²æ¡
if strncmpi(ColorBar,'On',2)
    if any(strncmpi(FigStyle,{'Auto','Triu'},4))
        colorbar('Location','EastOutside');
    else
        colorbar('Location','SouthOutside');
    end
end
end

% ---------------------------------------------------
%  è°æ´åæ è½´å»åº¦æ ç­¾å­å½æ°
% ---------------------------------------------------
function MyTickLabel(ha,tag)

%   æ ¹æ®æ¾ç¤ºèå´èªå¨è°æ´åæ è½´å»åº¦æ ç­¾çå½æ°
%   ha   åæ ç³»å¥æå¼
%   tag  è°æ´åæ è½´å»åº¦æ ç­¾çæ è¯å­ç¬¦ä¸²ï¼å¯ç¨åå¼å¦ä¸ï¼
%        'Auto' --- å°xè½´å»åº¦æ ç­¾æè½¬90åº¦ï¼yè½´å»åº¦æ ç­¾ä¸ä½è°æ´
%        'Tril' --- å°xè½´å»åº¦æ ç­¾æè½¬90åº¦ï¼å¹¶ä¾æ¬¡ç¼©è¿ï¼yè½´å»åº¦æ ç­¾ä¸ä½è°æ´
%        'Triu' --- å°xè½´å»åº¦æ ç­¾æè½¬90åº¦ï¼yè½´å»åº¦æ ç­¾ä¾æ¬¡ç¼©è¿
%   Example:
%   MyTickLabel(gca,'Tril');
%
%   CopyRightï¼xiezhhï¼è°¢ä¸­åï¼,2013.1ç¼å

if ~ishandle(ha)
    warning('MATLAB:warning2','ç¬¬ä¸ä¸ªè¾å¥åæ°åºä¸ºåæ ç³»å¥æ');
    return;
end

if ~strcmpi(get(ha,'type'),'axes')
    warning('MATLAB:warning3','ç¬¬ä¸ä¸ªè¾å¥åæ°åºä¸ºåæ ç³»å¥æ');
    return;
end

axes(ha);
xstr = get(ha,'XTickLabel');
xtick = get(ha,'XTick');
xl = xlim(ha);
ystr = get(ha,'YTickLabel');
ytick = get(ha,'YTick');
yl = ylim(ha);
set(ha,'XTickLabel',[],'YTickLabel',[]);
x = zeros(size(ytick)) + xl(1) - range(xl)/30;
y = zeros(size(xtick)) + yl(1) - range(yl)/70;
nx = numel(xtick);
ny = numel(ytick);

if strncmpi(tag,'Tril',4)
    y = y + (1:nx) - 1;
elseif strncmpi(tag,'Triu',4)
    x = x + (1:ny) - 1;
end

text(xtick,y,xstr,...
    'rotation',90,...
    'Interpreter','none',...
    'color','black',...
    'Fontsize',15,...
    'HorizontalAlignment','left','rotation',30);
text(x,ytick,ystr,...
    'Interpreter','none',...
    'color','black',...
    'Fontsize',15,...
    'HorizontalAlignment','right');
end

% ---------------------------------------------------
%  æ ¹æ®æ£ç¹æ°æ®ç»å¶3ç»´è²åå¾å­å½æ°
% ---------------------------------------------------
function  MyPatch(x,y,z,FigShape,FigSize)
%   æ ¹æ®æ£ç¹æ°æ®ç»å¶3ç»´è²åå¾
%   MyPatch(x,y,z,FigShape,FigSize)  x,y,zæ¯å®å¼æ°ç»ï¼ç¨æ¥æå®è²åä¸­å¿ç¹ä¸ç»´
%          åæ ãFigShapeæ¯å­ç¬¦ä¸²åéï¼ç¨æ¥æå®è²åå½¢ç¶ã
%          FigSizeæ¯å­ç¬¦ä¸²åéï¼ç¨æ¥æå®è²åå¤§å°ã
%
%   CopyRight:xiezhhï¼è°¢ä¸­åï¼, 2013.01 ç¼å
%
%   Exampleï¼
%         x = rand(10,1);
%         y = rand(10,1);
%         z = rand(10,1);
%         MyPatch(x,y,z,'s','Auto');
%

% è¾å¥åæ°ç±»åå¤æ­
if nargin < 3
    error('è³å°éè¦ä¸ä¸ªè¾å¥åæ°');
end
if ~isreal(x) || ~isreal(y) || ~isreal(z)
    error('åä¸ä¸ªè¾å¥åºä¸ºå®å¼æ°ç»');
end

n = numel(z);
if numel(x) ~= n || numel(y) ~= n
    error('åæ åºç­é¿');
end

if strncmpi(FigSize,'Auto',3) && ~strncmpi(FigShape,'Ellipse',1)
    id = (z == 0);
    x(id) = [];
    y(id) = [];
    z(id) = [];
end
if isempty(z)
    return;
end

% æ±è²åé¡¶ç¹åæ 
rab1 = ones(size(z));
maxz = max(abs(z));
if maxz == 0
    maxz = 1;
end
rab2 = abs(z)/maxz;
if strncmpi(FigShape,'Square',1)
    % æ¹å½¢
    if strncmpi(FigSize,'Full',3)
        r = rab1;
    else
        r = sqrt(rab2);
    end
    SquareVertices(x,y,z,r);
elseif strncmpi(FigShape,'Circle',1)
    % åå½¢
    if strncmpi(FigSize,'Full',3)
        r = 0.5*rab1;
    else
        r = 0.5*sqrt(rab2);
    end
    CircleVertices(x,y,z,r);
elseif strncmpi(FigShape,'Ellipse',1)
    % æ¤­åå½¢
    a = 0.48 + rab2*(0.57-0.48);
    b = (1-rab2).*a;
    EllipseVertices(x,y,z,a,b);
elseif strncmpi(FigShape,'Hexagon',1)
    % å­è¾¹å½¢
    if strncmpi(FigSize,'Full',3)
        r = 0.5*rab1;
    else
        r = 0.5*sqrt(rab2);
    end
    HexagonVertices(x,y,z,r);
else
    % è¡¨çå½¢
    if strncmpi(FigSize,'Full',3)
        r = 0.45*rab1;
    else
        r = 0.45*sqrt(rab2);
    end
    DialVertices(x,y,z,r);
end
end
%--------------------------------------------------
% æ±è²åé¡¶ç¹åæ å¹¶ç»å¶è²åçå­å½æ°
%--------------------------------------------------
function SquareVertices(x,y,z,r)
% æ¹å½¢
hx = r/2;
hy = hx;
Xp = [x-hx;x-hx;x+hx;x+hx;x-hx];
Yp = [y-hy;y+hy;y+hy;y-hy;y-hy];
Zp = repmat(z,[5,1]);
patch(Xp,Yp,Zp,'FaceColor','flat','EdgeColor','flat');
end

function CircleVertices(x,y,z,r)
% åå½¢
t = linspace(0,2*pi,30)';
m = numel(t);
Xp = repmat(x,[m,1])+cos(t)*r;
Yp = repmat(y,[m,1])+sin(t)*r;
Zp = repmat(z,[m,1]);
patch(Xp,Yp,Zp,'FaceColor','flat','EdgeColor','flat');
end

function EllipseVertices(x,y,z,a,b)
% æ¤­åå½¢
t = linspace(0,2*pi,30)';
m = numel(t);
t0 = -sign(z)*pi/4;
t0 = repmat(t0,[m,1]);
x0 = cos(t)*a;
y0 = sin(t)*b;
Xp = repmat(x,[m,1]) + x0.*cos(t0) - y0.*sin(t0);
Yp = repmat(y,[m,1]) + x0.*sin(t0) + y0.*cos(t0);
Zp = repmat(z,[m,1]);
patch(Xp,Yp,Zp,'FaceColor','flat','EdgeColor','flat');
end

function HexagonVertices(x,y,z,r)
% å­è¾¹å½¢
t = linspace(0,2*pi,7)';
m = numel(t);
Xp = repmat(x,[m,1])+cos(t)*r;
Yp = repmat(y,[m,1])+sin(t)*r;
Zp = repmat(z,[m,1]);
patch(Xp,Yp,Zp,'FaceColor','flat','EdgeColor','flat');
end

function DialVertices(x,y,z,r)
% è¡¨çå½¢
% ç»å¶è¡¨çæå½¢
maxz = max(abs(z));
t0 = z*2*pi/maxz-pi/2;
t0 = cell2mat(arrayfun(@(x)linspace(-pi/2,x,30)',t0,'UniformOutput',0));
m = size(t0,1);
r0 = repmat(r,[m,1]);
Xp = [x;repmat(x,[m,1]) + r0.*cos(t0);x];
Yp = [y;repmat(y,[m,1]) + r0.*sin(t0);y];
Zp = repmat(z,[m+2,1]);
patch(Xp,Yp,Zp,'FaceColor','flat','EdgeColor',[0,0,0]);

% ç»å¶è¡¨çåå¨
t = linspace(0,2*pi,30)';
m = numel(t);
Xp = repmat(x,[m,1])+cos(t)*r;
Yp = repmat(y,[m,1])+sin(t)*r;
Zp = repmat(z,[m,1]);
Xp = [Xp;flipud(Xp)];
Yp = [Yp;flipud(Yp)];
Zp = [Zp;flipud(Zp)];
patch(Xp,Yp,Zp,'FaceColor','flat','EdgeColor',[0,0,0]);
end

%--------------------------------------------------------------------------
%  è§£æè¾å¥åæ°å­å½æ°1
%--------------------------------------------------------------------------
function [FigShape,FigSize,FigStyle,FillStyle,DisplayOpt,TextColor,...
    XVarNames,YVarNames,ColorBar,GridOpt] = parseInputs(varargin)

if mod(nargin,2)~=0
    error('è¾å¥åæ°ä¸ªæ°ä¸å¯¹ï¼åºä¸ºæå¯¹åºç°');
end
pnames = {'FigShape','FigSize','FigStyle','FillStyle','DisplayOpt',...
    'TextColor','XVarNames','YVarNames','ColorBar','Grid'};
dflts =  {'Square','Full','Auto','Fill','On','k','','','Off','On'};
[FigShape,FigSize,FigStyle,FillStyle,DisplayOpt,TextColor,XVarNames,...
    YVarNames,ColorBar,GridOpt] = parseArgs(pnames, dflts, varargin{:});

validateattributes(FigShape,{'char'},{'nonempty'},mfilename,'FigShape');
validateattributes(FigSize,{'char'},{'nonempty'},mfilename,'FigSize');
validateattributes(FigStyle,{'char'},{'nonempty'},mfilename,'FigStyle');
validateattributes(FillStyle,{'char'},{'nonempty'},mfilename,'FillStyle');
validateattributes(DisplayOpt,{'char'},{'nonempty'},mfilename,'DisplayOpt');
validateattributes(TextColor,{'char','numeric'},{'nonempty'},mfilename,'TextColor');
validateattributes(XVarNames,{'char','cell'},{},mfilename,'XVarNames');
validateattributes(YVarNames,{'char','cell'},{},mfilename,'YVarNames');
validateattributes(ColorBar,{'char'},{'nonempty'},mfilename,'ColorBar');
validateattributes(GridOpt,{'char'},{'nonempty'},mfilename,'Grid');
if ~any(strncmpi(FigShape,{'Square','Circle','Ellipse','Hexagon','Dial'},1))
    error('å½¢ç¶åæ°åªè½ä¸ºSquare, Circle, Ellipse, Hexagon, Dial ä¹ä¸');
end
if ~any(strncmpi(FigSize,{'Full','Auto'},3))
    error('å¾å½¢å¤§å°åæ°åªè½ä¸ºFull, Auto ä¹ä¸');
end
if ~any(strncmpi(FigStyle,{'Auto','Tril','Triu'},4))
    error('å¾å½¢æ ·å¼åæ°åªè½ä¸ºAuto, Tril, Triu ä¹ä¸');
end
if ~any(strncmpi(FillStyle,{'Fill','NoFill'},3))
    error('å¾å½¢å¡«åæ ·å¼åæ°åªè½ä¸ºFill, NoFill ä¹ä¸');
end
if ~any(strncmpi(DisplayOpt,{'On','Off'},2))
    error('æ¾ç¤ºæ°å¼åæ°åªè½ä¸ºOnï¼Off ä¹ä¸');
end
if ~any(strncmpi(ColorBar,{'On','Off'},2))
    error('æ¾ç¤ºé¢è²æ¡åæ°åªè½ä¸ºOnï¼Off ä¹ä¸');
end
if ~any(strncmpi(GridOpt,{'On','Off'},2))
    error('æ¾ç¤ºç½æ ¼åæ°åªè½ä¸ºOnï¼Off ä¹ä¸');
end
end

%--------------------------------------------------------------------------
%  è§£æè¾å¥åæ°å­å½æ°2
%--------------------------------------------------------------------------
function [varargout] = parseArgs(pnames,dflts,varargin)
%   Copyright 2010-2011 The MathWorks, Inc.
%   $Revision: 1.1.6.2 $  $Date: 2011/05/09 01:27:26 $

% Initialize some variables
nparams = length(pnames);
varargout = dflts;
setflag = false(1,nparams);
unrecog = {};
nargs = length(varargin);

dosetflag = nargout>nparams;
dounrecog = nargout>(nparams+1);

% Must have name/value pairs
if mod(nargs,2)~=0
    m = message('stats:internal:parseArgs:WrongNumberArgs');
    throwAsCaller(MException(m.Identifier, '%s', getString(m)));
end

% Process name/value pairs
for j=1:2:nargs
    pname = varargin{j};
    if ~ischar(pname)
        m = message('stats:internal:parseArgs:IllegalParamName');
        throwAsCaller(MException(m.Identifier, '%s', getString(m)));
    end
    
    mask = strncmpi(pname,pnames,length(pname)); % look for partial match
    if ~any(mask)
        if dounrecog
            % if they've asked to get back unrecognized names/values, add this
            % one to the list
            unrecog((end+1):(end+2)) = {varargin{j} varargin{j+1}};
            continue
        else
            % otherwise, it's an error
            m = message('stats:internal:parseArgs:BadParamName',pname);
            throwAsCaller(MException(m.Identifier, '%s', getString(m)));
        end
    elseif sum(mask)>1
        mask = strcmpi(pname,pnames); % use exact match to resolve ambiguity
        if sum(mask)~=1
            m = message('stats:internal:parseArgs:AmbiguousParamName',pname);
            throwAsCaller(MException(m.Identifier, '%s', getString(m)));
        end
    end
    varargout{mask} = varargin{j+1};
    setflag(mask) = true;
end

% Return extra stuff if requested
if dosetflag
    varargout{nparams+1} = setflag;
    if dounrecog
        varargout{nparams+2} = unrecog;
    end
end
end