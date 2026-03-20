function [mean_fd,fd] = xic_fwd(filename)
        
        mp = textread(filename);
        mp(:, 1:3) = mp(:, 1:3) * 50;
        mp_diff = diff(mp);
        mp_dif = [zeros(1,6);mp_diff];
        mp_dif = abs(mp_dif);
        fd = sum(mp_dif,2);
        mean_fd = mean(fd);
end