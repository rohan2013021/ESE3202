
function the_graph = polyfit_graph(x,y,n)
    p1=polyfit(y,x,n)
    poly_val=polyval(p1,y)
    subplot(1,2,1)
    plot(poly_val,y)
    subplot(1,2,2)
    plot(y,x)
end