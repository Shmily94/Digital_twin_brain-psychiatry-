
%% check cpm predict performance

clear;clc;

cd('CPM_results\')
name = {'SST:stop success','SST:stop failure','SST:go wrong',...
       'MID:feedmiss','MID:feedhit','MID: antici hit'};
model_name = {'_SST_stopsuc.mat','_SST_stopfai.mat' ...
        'SST_gowrong.mat','feed_miss.mat','feed_hit.mat' ...
        'antici_hit.mat'};

 number=[1 3 2 4 5 6]; % resort behavioral variable
 dis_names  = {'adhd','cd' ,'anxiety','dep','eat','speph'};

[BL_Exter_beha,BL_Inter_beha,BL_Pheno_residual_match_sub] = xic_CPM_beha;

for  j = 1:6
    models = dir(['*',model_name{j}]);
    for i = 1:length(models)
        disp([i,j])
        load(fullfile(models(i).folder,models(number(i)).name))
        R_pos_neg_both(1,i)= (CPM_Result.pos_r_mean);
        R_pos_neg_both(2,i)= (CPM_Result.neg_r_mean);
        R_pos_neg_both(3,i)= (CPM_Result.both_r_mean);
        R_subject(i,j) = length(CPM_Result.subject);
 
        R_predict_pos(j,i) = CPM_Result.pos_r_mean;
        R_predict_neg(j,i) = CPM_Result.neg_r_mean;
        R_predict_both(j,i) = CPM_Result.both_r_mean;
   end
end

save FU2_R_predict_perform.mat  R_predict_pos R_predict_neg R_predict_both 


%% Identify NP factor
clear;clc

path_model = '\CPM_Models';

model_name = {'_SST_stopsuc.mat','_SST_stopfai.mat' ...
        'SST_gowrong.mat','feed_miss.mat','feed_hit.mat' ...
        'antici_hit.mat'};
 
name = {'SST:stop success','SST:stop failure','SST:go wrong',...
       'MID:feedmiss','MID:feedhit','MID: antici hit'};

number=[1 3 2 4 5 6]; % resort behavioral variable
dis_names  = {'adhd','cd' ,'anxiety','dep','eat','speph'};
mask_id = reshape(1:6*6,6,6);
mask = reshape(tril(reshape(1:6*6,6,6),-1),[],1); 
exter_mask = [2]; adhd - cd
inter_mask = [16 17 18 23 24 30];
across_mask = [3 4 5 6 9 10 11 12]; % internal - external
mask_id_all = tril(reshape(1:268*268,268,268),-1);

for k= 1:6

    models = dir(fullfile(path_model,['*',model_name{k}]));

    for i=1:6
        disp(i)
        
            model1 = load(fullfile(path_model,models(number(i)).name));
            network1_neg = model1.CPM_Result.neg_mask;  network1_neg(network1_neg<0.95)=0;network1_neg(network1_neg>0)=1;
            network1_pos = model1.CPM_Result.pos_mask;  network1_pos(network1_pos<0.95)=0;network1_pos(network1_pos>0)=1;

        for j=1:6
        
            if i~=j
   
                model2 = load(fullfile(path_model,models(number(j)).name));
                network2_neg = model2.CPM_Result.neg_mask;network2_neg(network2_neg<0.95)=0;network2_neg(network2_neg>0)=1;
                network2_pos = model2.CPM_Result.pos_mask;network2_pos(network2_pos<0.95)=0;network2_pos(network2_pos>0)=1;

                neg_pos =network1_neg.*network2_pos; neg_pos_id = mask_id_all(neg_pos>0); neg_pos_id(neg_pos_id==0)=[];
                neg_neg =network1_neg.*network2_neg; neg_neg_id = mask_id_all(neg_neg>0); neg_neg_id(neg_neg_id==0)=[];
                pos_pos =network1_pos.*network2_pos; pos_pos_id = mask_id_all(pos_pos>0); pos_pos_id(pos_pos_id==0)=[];
                pos_neg =network1_pos.*network2_neg; pos_neg_id = mask_id_all(pos_neg>0); pos_neg_id(pos_neg_id==0)=[];

                neg_pos_all{i,j} =neg_pos;    neg_pos_all_id{i,j} =neg_pos_id;  
                neg_neg_all{i,j} =neg_neg;    neg_neg_all_id{i,j} =neg_neg_id; 
                pos_neg_all{i,j} =pos_neg;    pos_neg_all_id{i,j} =pos_neg_id;
                pos_pos_all{i,j} =pos_pos;    pos_pos_all_id{i,j} =pos_pos_id;

                neg_neg_num(i,j) = sum(neg_neg(:))/2;
                pos_pos_num(i,j) = sum(pos_pos(:))/2;

                pos_neg_num(i,j) = sum(pos_neg(:))/2;
                neg_pos_num(i,j) = sum(neg_pos(:))/2;
                
                opposite = pos_neg_num(i,j) + neg_pos_num(i,j);
                samesite = neg_neg_num(i,j) + pos_pos_num(i,j);
                all = (opposite+samesite);

                [h, p, stats] = fishertest([round(all/2) all-round(all/2);samesite opposite]);

                odd(i,j) =  stats.OddsRatio;

            end

        end

    end
    
    odd_all{k} = odd;
    
    disp(['Overlaped edges'])
  
    neg_pos_all_dimension_id{k} =neg_pos_all_id;     oppo_neg_pos_all_dimension_id{k} = unique_cell(neg_pos_all_id(across_mask));     
    neg_neg_all_dimension_id{k} =neg_neg_all_id;     oppo_neg_neg_all_dimension_id{k} = unique_cell(neg_neg_all_id(across_mask));    
    pos_neg_all_dimension_id{k} =pos_neg_all_id;     oppo_pos_neg_all_dimension_id{k} = unique_cell(pos_neg_all_id(across_mask));   
    pos_pos_all_dimension_id{k} =pos_pos_all_id;     oppo_pos_pos_all_dimension_id{k} = unique_cell(pos_pos_all_id(across_mask));    
    
    exter_neg_pos_all_dimension_id{k} = unique_cell(neg_pos_all_id(exter_mask));  inter_neg_pos_all_dimension_id{k} = unique_cell(neg_pos_all_id(inter_mask));  
    exter_neg_neg_all_dimension_id{k} = unique_cell(neg_neg_all_id(exter_mask)); inter_neg_neg_all_dimension_id{k} = unique_cell(neg_neg_all_id(inter_mask));
    exter_pos_neg_all_dimension_id{k} = unique_cell(pos_neg_all_id(exter_mask));  inter_pos_neg_all_dimension_id{k} = unique_cell(pos_neg_all_id(inter_mask));
    exter_pos_pos_all_dimension_id{k} = unique_cell(pos_pos_all_id(exter_mask)); inter_pos_pos_all_dimension_id{k} = unique_cell(pos_pos_all_id(inter_mask));

    neg_pos_all_dimension{k} =neg_pos_all;    
    neg_neg_all_dimension{k} =neg_neg_all;    
    pos_neg_all_dimension{k} =pos_neg_all;    
    pos_pos_all_dimension{k} =pos_pos_all;    

    oppo_way = pos_neg_num + neg_pos_num; oppo_way_num =reshape(oppo_way,[],1);
    same_way = neg_neg_num + pos_pos_num; same_way_num =reshape(same_way,[],1);
    
    same_way_all{k} = same_way;
    oppo_way_all{k} = oppo_way;
    overall_way_all(k,1) =  sum(oppo_way_num(mask>0)) +  sum(same_way_num(mask>0));
    overall_way_same(k,1) = sum(same_way_num(mask>0));
    overall_way_oppo(k,1) = sum(oppo_way_num(mask>0));
    
    inter_same_all(k,1) = sum(same_way_num(inter_mask));
    exter_same_all(k,1) = sum(same_way_num(exter_mask));
    across_same_all(k,1) = sum(same_way_num(across_mask));
    
    inter_oppo_all(k,1) = sum(oppo_way_num(inter_mask));
    exter_oppo_all(k,1) = sum(oppo_way_num(exter_mask));
    across_oppo_all(k,1) = sum(oppo_way_num(across_mask));
    
    % pos-pos,neg-neg, pos-neg,neg-pos, separetly
    
    pos_pos = reshape(pos_pos_num,[],1);neg_neg = reshape(neg_neg_num,[],1);
    pos_neg = reshape(pos_neg_num,[],1);neg_pos = reshape(neg_pos_num,[],1);
    
    inter_ppnn_all(k,:) = [sum(pos_pos(inter_mask)),sum(neg_neg(inter_mask))]; 
    exter_ppnn_all(k,:) = [sum(pos_pos(exter_mask)),sum(neg_neg(exter_mask))]; 
    oppo_pnnp_ppnn_all(k,:) = [sum(pos_neg(across_mask)),sum(neg_pos(across_mask)),sum(pos_pos(across_mask)),sum(neg_neg(across_mask))];
    
end

%% summary results

TableS4_1 = table;
TableS4_1.name = name';
TableS4_1.num_all = overall_way_all;
TableS4_1.num_same = overall_way_same;
TableS4_1.num_oppo = overall_way_oppo;

conditions = [1 2 3 4 5 6];
Same_inter = inter_same_all(conditions); Same_exter = exter_same_all(conditions);Same_between = across_same_all(conditions);
Oppo_inter = inter_oppo_all(conditions); Oppo_exter = exter_oppo_all(conditions);Oppo_between = across_oppo_all(conditions);
inter_ppnn = inter_ppnn_all(conditions,:);exter_ppnn = exter_ppnn_all(conditions,:);oppo_PnnpPpnn = oppo_pnnp_ppnn_all(conditions,:);
All_data = [Same_inter,Same_exter,Same_between,Oppo_inter,Oppo_exter,Oppo_between]';

% generate the Table S4,S5,S6  
All_data = [round(mean(All_data,2)),All_data];
TableS5 = table;
TableS5.group = {'Within_Inter';'Within_Exter';'Between_In_Ex';'Within_Inter';'Within_Exter';'Between_In_Ex'};
TableS5.type = [repmat({'Same_overappling'},3,1);repmat({'Oppo_overappling'},3,1)];
TableS5.Mean_value = All_data(:,1);
TableS5.SST_stop_sucess = All_data(:,2);
TableS5.SST_stop_failure= All_data(:,3);
TableS5.SST_go_wrong= All_data(:,4);
TableS5.MID_feedmiss= All_data(:,5);
TableS5.MID_feedhit = All_data(:,6);
TableS5.MID_anticip = All_data(:,7);
TableS5 = TableS5([2 5 1 4 3 6],:);


paried_id = [2 4; 1 5; 6 3];

for i=1:7
    for j = 1:3
    group1 = All_data(paried_id(j,1),i); group2 =  All_data(paried_id(j,2),i);
    [h, p, stats] = fishertest([group1 group2; round((group1+group2)*(6/22)) (group1+group2)-round((group1+group2)*(6/22))]);
    Odd_value(j,i) = stats.OddsRatio;

    end
end

TableS4_2 = table;
TableS4_2.group = {'Externalising','Internalising','External-Internalising'}';
TableS4_2.type = [repmat({'Same_overappling VS Oppositive'},3,1)];
TableS4_2.Mean_value = Odd_value(:,1);
TableS4_2.SST_stop_sucess = Odd_value(:,2);
TableS4_2.SST_stop_failure= Odd_value(:,3);
TableS4_2.SST_go_wrong= Odd_value(:,4);
TableS4_2.MID_feedmiss= Odd_value(:,5);
TableS4_2.MID_feedhit= Odd_value(:,6);
TableS4_2.MID_anticip= Odd_value(:,7);


% Table S6. contains the num
data_ppnn =  [exter_ppnn,inter_ppnn,oppo_PnnpPpnn]';
data_ppnn =  round([mean(data_ppnn,2),data_ppnn]);

paried_id = [1 2;3 4;5 6; 7 8];

for j=1:7
    for i=1:4
        
    group1 = data_ppnn(paried_id(i,1),j); group2 = data_ppnn(paried_id(i,2),j);
    group_id = sort([group1 group2],'descend');
    [h, p, stats] = fishertest([group_id(1) group_id(2);round(sum(group_id)/2) sum(group_id)-round((sum(group_id))/2)]);
    Odd_value(i,j) = stats.OddsRatio;
    Odd_value_P(i,j) = p;
    
    end
end

data_all = [data_ppnn(1:2,:);Odd_value(1,:); ...
            data_ppnn(3:4,:);Odd_value(2,:); ...
            data_ppnn(5:6,:);Odd_value(3,:); ...
            data_ppnn(7:8,:);Odd_value(4,:)];

TableS6_across = table();

TableS6_across.type = [repmat({'Exter-network'},3,1);repmat({'Inter-network'},3,1);repmat({'Trans-network'},6,1)];
TableS6_across.group = [repmat({'Pos-Pos';'Neg-Neg';'PP VS. NN'},2,1);{'Pos-Neg';'Neg-Pos';'PN VS. NP'};{'Pos-Pos';'Neg-Neg';'PP VS. NN'}];
TableS6_across.Mean_value = data_all(:,1);
TableS6_across.SST_stop_sucess_num = data_all(:,2);
TableS6_across.SST_stop_sucess_id = {exter_pos_pos_all_dimension_id{1};exter_neg_neg_all_dimension_id{1};{};inter_pos_pos_all_dimension_id{1};inter_neg_neg_all_dimension_id{1};{}; ...
                                                                 oppo_pos_neg_all_dimension_id{1};oppo_neg_pos_all_dimension_id{1};{}; ...
                                                                 oppo_pos_pos_all_dimension_id{1};oppo_neg_neg_all_dimension_id{1};{}}; 
TableS6_across.SST_stop_failure_num= data_all(:,3);
TableS6_across.SST_stop_failure_id  = {exter_pos_pos_all_dimension_id{2};exter_neg_neg_all_dimension_id{2};{};inter_pos_pos_all_dimension_id{2};inter_neg_neg_all_dimension_id{2};{}; ...
                                                                 oppo_pos_neg_all_dimension_id{2};oppo_neg_pos_all_dimension_id{2};{}; ...
                                                                 oppo_pos_pos_all_dimension_id{2};oppo_neg_neg_all_dimension_id{2};{}}; 
TableS6_across.SST_go_wrong_num= data_all(:,4);
TableS6_across.SST_go_wrong_id  = {exter_pos_pos_all_dimension_id{3};exter_neg_neg_all_dimension_id{3};{};inter_pos_pos_all_dimension_id{3};inter_neg_neg_all_dimension_id{3};{}; ...
                                                                 oppo_pos_neg_all_dimension_id{3};oppo_neg_pos_all_dimension_id{3};{}; ...
                                                                 oppo_pos_pos_all_dimension_id{3};oppo_neg_neg_all_dimension_id{3};{}}; 
TableS6_across.MID_feedmiss_num= data_all(:,5);
TableS6_across.MID_feedmiss_id  = {exter_pos_pos_all_dimension_id{4};exter_neg_neg_all_dimension_id{4};{};inter_pos_pos_all_dimension_id{4};inter_neg_neg_all_dimension_id{4};{}; ...
                                                                 oppo_pos_neg_all_dimension_id{4};oppo_neg_pos_all_dimension_id{4};{}; ...
                                                                 oppo_pos_pos_all_dimension_id{4};oppo_neg_neg_all_dimension_id{4};{}}; 
TableS6_across.MID_feedhit_num = data_all(:,6);
TableS6_across.MID_feedhit_id          =  {exter_pos_pos_all_dimension_id{5};exter_neg_neg_all_dimension_id{5};{};inter_pos_pos_all_dimension_id{5};inter_neg_neg_all_dimension_id{5};{}; ...
                                                                 oppo_pos_neg_all_dimension_id{5};oppo_neg_pos_all_dimension_id{5};{}; ...
                                                                 oppo_pos_pos_all_dimension_id{5};oppo_neg_neg_all_dimension_id{5};{}};                                                       
TableS6_across.MID_anticip_num= data_all(:,7);
TableS6_across.MID_anticip_id           =  {exter_pos_pos_all_dimension_id{6};exter_neg_neg_all_dimension_id{6};{};inter_pos_pos_all_dimension_id{6};inter_neg_neg_all_dimension_id{6};{}; ...
                                                                 oppo_pos_neg_all_dimension_id{6};oppo_neg_pos_all_dimension_id{6};{}; ...
                                                                 oppo_pos_pos_all_dimension_id{6};oppo_neg_neg_all_dimension_id{6};{}};
                                                             
                                                     
TableS6.TableS6_across  = TableS6_across;

save Network_P_factor.mat same_way_all oppo_way_all neg_pos_all_dimension neg_neg_all_dimension ...
    pos_neg_all_dimension pos_pos_all_dimension  TableS4_1 TableS4_2 TableS5 TableS6 

 
