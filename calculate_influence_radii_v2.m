clc

close all
clear all

com.comsol.model.util.ModelUtil.showProgress(true);

borehole_spacing = [20 30 40 50 60 70 80 90 100 110 120 130 140];

xlsx_name = 'results_influence_radii_v2.xlsx';

T = readtable(xlsx_name);

for i = 1:height(T)
    
    geology = lower(T.Geology{i});
    geology = replace(geology, '-', '_');
    
    base_name = sprintf('geology_%s_%dm_20m_without_groundwater_flow', geology, T.L_borehole(i));
    
    mph_name = sprintf('Shallow_Geothermal_Potential_Models\\%s.mph', base_name);
    png_name = sprintf('Shallow_Geothermal_Potential_Models\\%s.png', base_name);
    
    model = mphload(mph_name);
    
    if T.L_borehole(i) == 100
        x = [5, 10, 15];
    elseif T.L_borehole(i) == 200
        x = [15, 25, 35];
    else
        error('Invalid borehole length: %d m.', T.L_borehole(i));
    end
    
    for j = 1:length(borehole_spacing)
        
        column_name = T.Properties.VariableNames{j+2};

        E = table2array(T(i, j+2));
        
        if ~isnan(E)
            fprintf(1, '*** Skipping geology=%s L_borehole=%s borehole_spacing=%s column_name=%s E_max=%s\n', T.Geology{i}, num2str(T.L_borehole(i)), num2str(borehole_spacing(j)), column_name, num2str(E));
            continue
        else
            fprintf(1, '*** Calculating geology=%s L_borehole=%s borehole_spacing=%s column_name=%s\n', T.Geology{i}, num2str(T.L_borehole(i)), num2str(borehole_spacing(j)), column_name);
        end
        
        model.param.set('borehole_spacing', sprintf('%s[m]', num2str(borehole_spacing(j))));
        
        y = zeros(1, length(x));
        
        for k = 1:length(x)
            
            model.param.set('E_annual', sprintf('%s[MWh]', num2str(x(k))));
            
            model.sol('sol1').runAll;
            
            y(k) = min(mphglobal(model, 'T_ave', 'unit', 'degC'));
            
        end
        
        p = polyfit(x, y, 1);
        
        xi = linspace(0, 40, 100);
        yi = polyval(p, xi);
        
        SS_res = sum((y - polyval(p, x)).^2);
        SS_tot = sum((y - mean(y)).^2);
        
        R_squared = 1 - SS_res / SS_tot;
        
        RMSE = sqrt(mean((y - polyval(p, x)).^2));
        
        T(i, j+2) = {-p(2)/p(1)};
        
        fprintf(1, '*** E_max=%s\n', table2array(T(i,j+2)));
        
        writetable(T, xlsx_name);
        
        close all
        figure
        subplot(121)
        plot(x, y, 'bo', xi, yi, 'r-')
        xlim = get(gca, 'xlim');
        ylim = get(gca, 'ylim');
        hold on
        plot(table2array(T(i,j+2)), 0, 'ko')
        plot([xlim(1) table2array(T(i,j+2)) table2array(T(i,j+2))], [0 0 ylim(2)], 'k-')
        hold off
        title(sprintf('base_name=%s\nE_max=%.3f R^2=%.6f RMSE=%.6f', base_name, table2array(T(i,j+2)), R_squared, RMSE), 'interpreter', 'none')
        subplot(122)
        plot(borehole_spacing, table2array(T(i, 3:end)), 'ro-')
        pause(1)
        
    end
    
    print('-dpng2', png_name)
    
end
