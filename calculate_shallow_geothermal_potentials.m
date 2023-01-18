clc

close all
clear all

com.comsol.model.util.ModelUtil.showProgress(true);

xlsx_name = 'results_shallow_geothermal_potentials.xlsx';

T = readtable(xlsx_name);

for i = 1:height(T)

    if ~isnan(T.E_max(i))
        fprintf(1, '*** Skipping geology=%s L_borehole=%s borehole_spacing=%s E_max=%s\n', T.Geology{i}, num2str(T.L_borehole(i)), num2str(T.borehole_spacing(i)), num2str(T.E_max(i)));
        continue
    else
        fprintf(1, '*** Calculating geology=%s L_borehole=%s borehole_spacing=%s\n', T.Geology{i}, num2str(T.L_borehole(i)), num2str(T.borehole_spacing(i)));
    end
    
    geology = lower(T.Geology{i});
    geology = replace(geology, '-', '_');
    
    if strcmp(T.darcy_flux{i}, 'ignored')
        base_name = sprintf('geology_%s_%dm_%dm_without_groundwater_flow', geology, T.L_borehole(i), T.borehole_spacing(i));
    else
        base_name = sprintf('geology_%s_%dm_%dm_with_groundwater_flow', geology, T.L_borehole(i), T.borehole_spacing(i));
    end
    
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
    
    T.E_max(i) = -p(2) / p(1);
    
    fprintf(1, '*** E_max=%s\n', num2str(T.E_max(i)));
    
    writetable(T, xlsx_name);
    
    close all
    figure
    plot(x, y, 'bo', xi, yi, 'r-')
    xlim = get(gca, 'xlim');
    ylim = get(gca, 'ylim');
    hold on
    plot(T.E_max(i), 0, 'ko')
    plot([xlim(1) T.E_max(i) T.E_max(i)], [0 0 ylim(1)], 'k-')
    hold off
    title(sprintf('base_name=%s\nE_max=%.3f R^2=%.6f RMSE=%.6f', base_name, T.E_max(i), R_squared, RMSE), 'interpreter', 'none')
    print('-dpng2', png_name)
    pause(1)

end
