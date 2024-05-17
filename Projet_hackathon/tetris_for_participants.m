classdef Block
    properties
        type
        value
        color
        rot
        width
        height
        mask
    end
    
    methods
        function obj = Block(type)
            if nargin > 0
                obj.type = type;
                obj.mask = {};
                if type == 0
                    obj.value = 1;
                    obj.color = [255, 0, 0];
                    obj.rot = 2;
                    obj.width = [1, 2];
                    obj.height = [2, 1];
                    obj.mask{1} = [1, 0; 1, 0];
                    obj.mask{2} = [0, 0; 1, 1];
                elseif type == 1
                    obj.value = 2;
                    obj.color = [0, 0, 255];
                    obj.rot = 1;
                    obj.width = [2];
                    obj.height = [2];
                    obj.mask{1} = [1, 1; 1, 1];
                elseif type == 2
                    obj.value = 3;
                    obj.color = [155, 50, 200];
                    obj.rot = 2;
                    obj.width = [2, 3];
                    obj.height = [3, 2];
                    obj.mask{1} = [1, 0; 1, 1; 0, 1];
                    obj.mask{2} = [0, 1, 1; 1, 1, 0];
                elseif type == 3
                    obj.value = 4;
                    obj.color = [200, 150, 55];
                    obj.rot = 2;
                    obj.width = [2, 3];
                    obj.height = [3, 2];
                    obj.mask{1} = [0, 1; 1, 1; 1, 0];
                    obj.mask{2} = [1, 1, 0; 0, 1, 1];
                elseif type == 4
                    obj.value = 5;
                    obj.color = [55, 200, 200];
                    obj.rot = 4;
                    obj.width = [3, 2, 3, 2];
                    obj.height = [2, 3, 2, 3];
                    obj.mask{1} = [1, 0, 0; 1, 1, 1];
                    obj.mask{2} = [0, 1; 0, 1; 1, 1];
                    obj.mask{3} = [1, 1, 1; 0, 0, 1];
                    obj.mask{4} = [1, 1; 1, 0; 1, 0];
                elseif type == 5
                    obj.value = 6;
                    obj.color = [50, 70, 150];
                    obj.rot = 4;
                    obj.width = [3, 2, 3, 2];
                    obj.height = [2, 3, 2, 3];
                    obj.mask{1} = [0, 0, 1; 1, 1, 1];
                    obj.mask{2} = [1, 1; 0, 1; 0, 1];
                    obj.mask{3} = [1, 1, 1; 1, 0, 0];
                    obj.mask{4} = [1, 0; 1, 0; 1, 1];
                elseif type == 6
                    obj.value = 7;
                    obj.color = [150, 30, 150];
                    obj.rot = 2;
                    obj.width = [1, 3];
                    obj.height = [3, 1];
                    obj.mask{1} = [1, 0, 0; 1, 0, 0; 1, 0, 0];
                    obj.mask{2} = [0, 0, 0; 0, 0, 0; 1, 1, 1];
                else
                    obj.value = -1;
                    obj.color = [0, 0, 0];
                    obj.width = 1;
                    obj.height = 1;
                    obj.mask = {};
                end
            end
        end
        
        function printBlock(obj, rot)
            if nargin < 2
                rot = 1;
            end
            Nb = max(obj.width(rot), obj.height(rot));
            ColorArray = uint8(255 * ones(Nb, Nb, 3));
            for i = 1:obj.width(rot)
                for j = 1:obj.height(rot)
                    if obj.mask{rot}(end + 1 - j, i) == 1
                        ColorArray(end + 1 - j, i, :) = obj.color;
                    end
                end
            end
            imshow(ColorArray, 'InitialMagnification', 'fit');
            hold on;
            for i = 1:Nb
                plot([0.5, Nb + 0.5], [i - 0.5, i - 0.5], 'k');
                plot([i - 0.5, i - 0.5], [0.5, Nb + 0.5], 'k');
            end
            hold off;
        end
    end
end

classdef ActionGene
    properties
        trans
        rot
    end
    
    methods
        function obj = ActionGene(x, r)
            obj.trans = x;
            obj.rot = r;
        end
    end
end

classdef GameState
    properties
        grid
        block
        list_actions
    end
    
    methods
        function obj = GameState(grid, block, list_actions)
            obj.grid = grid;
            obj.block = block;
            obj.list_actions = list_actions;
        end
    end
end

classdef Game
    properties
        L
        H
        grid
        block_list
        list_block
        history_block
        actions
        current_block
        fig_grid
    end
    
    methods
        function obj = Game(L, H, fig, list_block)
            if nargin < 3
                fig = false;
            end
            if nargin < 4
                list_block = [];
            end
            obj.L = L;
            obj.H = H;
            obj.grid = zeros(H, L);
            obj.block_list = {};
            obj.list_block = list_block;
            obj.history_block = [];
            obj.actions = {};
            Nbloc = 7;
            for i = 0:(Nbloc - 1)
                blk = Block(i);
                obj.block_list{end + 1} = blk;
                b_action = {};
                for r = 1:blk.rot
                    b_action{end + 1} = 0:(L - blk.width(r));
                end
                obj.actions{end + 1} = b_action;
            end
            if ~isempty(list_block)
                obj.current_block = list_block(1);
            else
                obj.current_block = randi(Nbloc) - 1;
            end
            if fig
                obj.fig_grid = figure;
                subplot(1, 2, 1);
                title('Game State');
                subplot(1, 2, 2);
                title('Current Block');
            end
        end
        
        function s = returnGameState(obj)
            s = GameState(obj.grid, obj.block_list{obj.current_block + 1}, obj.actions{obj.current_block + 1});
        end
        
        function game_over = updateGameState(obj, ag)
            rot = ag.rot;
            trans = ag.trans;
            b = obj.block_list{obj.current_block + 1};
            y_max = obj.findMaxY(b, ag);
            if y_max < 0
                game_over = true;
                return;
            end
            game_over = false;
            for k = 1:b.width(rot)
                x_scan = trans + k - 1;
                for l = 1:b.height(rot)
                    y_scan = y_max - l + 1;
                    if obj.grid(y_scan, x_scan) == 0
                        obj.grid(y_scan, x_scan) = b.mask{rot}(end + 1 - l, k) * b.value;
                    end
                end
            end
            obj.history_block(end + 1) = obj.current_block;
            if ~isempty(obj.list_block) && length(obj.list_block) > length(obj.history_block)
                obj.current_block = obj.list_block(length(obj.history_block) + 1);
            elseif length(obj.list_block) == length(obj.history_block)
                game_over = true;
                disp("You used all the blocks in the list");
            else
                obj.current_block = randi(7) - 1;
            end
        end
        
        function y_max = findMaxY(obj, b, ag)
            rot = ag.rot;
            x = ag.trans;
            ymax = obj.H - 1;
            y_max_list = ones(1, b.width(rot)) * (obj.H - 1);
            for k = 1:b.width(rot)
                x_scan = x + k - 1;
                for j = 1:obj.H
                    if obj.grid(j, x_scan) > 0
                        y_max_list(k) = j - 1;
                        break;
                    end
                end
            end
            y_max = min(y_max_list);
            for k = 1:b.width(rot)
                x_scan = x + k - 1;
                for l = 1:b.height(rot)
                    y_scan = y_max - l + 1;
                    if y_scan < 1
                        y_max = -1;
                        return;
                    elseif obj.grid(y_scan, x_scan) > 0 && b.mask{rot}(end + 1 - l, k) > 0
                        y_max = -1;
                        return;
                    end
                end
            end
        end
        
        function printGrid(obj)
            imshow(obj.grid, 'InitialMagnification', 'fit');
            colormap([0, 0, 0; 1, 0, 0; 0, 0, 1; 155/255, 50/255, 200/255; 200/255, 150/255, 55/255; 55/255, 200/255, 200/255; 50/255, 70/255, 150/255; 150/255, 30/255, 150/255]);
            grid on;
            xticks(1:obj.L);
            yticks(1:obj.H);
            set(gca, 'YDir', 'reverse');
        end
        
        function printState(obj)
            if isempty(obj.fig_grid) || ~isvalid(obj.fig_grid)
                obj.fig_grid = figure;
                subplot(1, 2, 1);
                title('Game State');
                subplot(1, 2, 2);
                title('Current Block');
            end
            subplot(1, 2, 1);
            obj.printGrid();
            subplot(1, 2, 2);
            b = obj.block_list{obj.current_block + 1};
            b.printBlock();
        end
    end
end

