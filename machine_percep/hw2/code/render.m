function [img] = render( img, p2d, polygons, color)
    lineShapeInserter = vision.ShapeInserter('Shape', 'Lines', 'BorderColor', 'Black', 'LineWidth', 5, 'Opacity', 1);
    polygonShapeInserter = vision.ShapeInserter('Shape', 'Polygons', 'Fill', true, 'Opacity', 1, ...
                                                'BorderColor', 'Custom', 'CustomBorderColor', color, ...
                                                'FillColor', 'Custom', 'CustomFillColor', color);
                                                                                 
    [n, m] = size(polygons);
    for i = 1:n
        c = reshape(p2d(polygons(i,:),1:2)', 1, 2*m);
        img = step(polygonShapeInserter, img, int32(c));
        for j = 1:m-1
            img = step(lineShapeInserter, img, int32([p2d(polygons(i,j),1); p2d(polygons(i,j),2); ... 
                                                      p2d(polygons(i,j+1),1); p2d(polygons(i,j+1),2)]));
        end;
        img = step(lineShapeInserter, img, int32([p2d(polygons(i,m),1); p2d(polygons(i,m),2); ... 
                                                  p2d(polygons(i,1),1); p2d(polygons(i,1),2)]));
    end
end

