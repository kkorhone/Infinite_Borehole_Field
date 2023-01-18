clc; clear all

model_files = dir('geology_*.mph');
model_names = {model_files.name};

com.comsol.model.util.ModelUtil.showProgress(true);

borehole_spacing = [20 30 40 50 60 70 80 90 100 110 120 130 140];

X = zeros(length(model_names), length(borehole_spacing));

for i = 1:length(model_names)
    
    model = mphload(model_names{i});
    
    L_borehole = model.param.evaluate('L_borehole');
    
    fprintf(1, '*** Using model %s (L_borehole=%s)\n', model_names{i}, num2str(L_borehole));
    
    if L_borehole == 100
        x = [5, 10, 15];
    elseif L_borehole == 200
        x = [15, 25, 35];
    else
        error('Invalid borehole length: %d m.', L_borehole);
    end
    
    close all
    
    for j = 1:length(borehole_spacing)
        
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
        
        X(i, j) = -p(2) / p(1);
        
        clf; subplot(121); plot(x, y, 'bo', xi, yi, 'r-', X(i,j), 0, 'ko'); subplot(122); plot(borehole_spacing(1:j), X(i,1:j), 'ro-'); pause(1)
        
        fprintf(1, '*** Solved borehole_spacing=%s E_max=%s\n', num2str(borehole_spacing(j)), num2str(-p(2)/p(1)));
        
        save('results_influence_radius_v3.mat', 'model_names', 'borehole_spacing', 'X')
        
    end
    
end
