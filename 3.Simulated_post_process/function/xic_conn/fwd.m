function [mat, fwd_percent] = fwd(subj_numb, filename, exit_file, csv_file, run)
        mat = textread(filename);
        radius = 50; %mm
        ts = mat;
        temp = mat(:,4:6)*180/pi; %convert to degrees
        temp = (2*radius*pi/360)*temp;
        ts(:,4:6) = temp;
        dts = diff(ts);
        fwd = sum(abs(dts),2);
        a = 0.0;
        fwd = [a;fwd];
        mat = [mat fwd];
        fwd_1 = fwd>0.2;
        fwd_ex = fwd(fwd_1);
        fwd_percent = (size(fwd_ex)/size(fwd))*100;
        fwd_percent = round(fwd_percent);
        
        fid = fopen(exit_file,'a+');
        fprintf(fid,'%s has %d percent volumes higher than 0.2 in %s\n',subj_numb,fwd_percent,run);
        fclose(fid);
        
        mat = array2table(mat);
        writetable(mat,csv_file)
end