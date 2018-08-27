
     d3.json("/massage/", function (error, massage) {

          if (error)
                console.log(error);
            console.log(massage);
    var svg = d3.select("#speedometer")
                .append("svg:svg")
                .attr("width", 500)
                .attr("height", 500);


   var gauge = iopctrl.arcslider()
                .radius(120)   //仪表盘的半径
                .events(false)
                .indicator(iopctrl.defaultGaugeIndicator);
        gauge.axis().orient("in")
                .normalize(true)
                .ticks(12)  //数字之间的刻度大小
                .tickSubdivide(2)   //当前刻度与下一刻度之间的格挡个数
                .tickSize(10, 8, 10)
                .tickPadding(10)   //数字距离刻度的距离
                .scale(d3.scale.linear()
                        .domain([0,15])   //刻度范围，投资级数，内圈
                        .range([-3*Math.PI/4, 3*Math.PI/4]));  //刻度盘的周长

   var gauge1 = iopctrl.arcslider()
                .radius(170)   //仪表盘的半径
                .events(false)
                .indicator(iopctrl.defaultGaugeIndicator);
        gauge1.axis().orient("in")
                .normalize(true)
                .ticks(12)  //数字之间的刻度大小
                .tickSubdivide(3)   //当前刻度与下一刻度之间的格挡个数
                .tickSize(10, 8, 10)
                .tickPadding(10)   //数字距离刻度的距离
                .scale(d3.scale.linear()
                        .domain([-5,10])   //刻度范围,回报率,外圈
                        .range([-3*Math.PI/4, 3*Math.PI/4]));  //刻度盘的周长

   var segDisplay = iopctrl.segdisplay()
                .width(80)  //蓝色数字的宽度
                .digitCount(5)   //蓝色数字的位数
                .negative(false)
                .decimals(0);

        svg.append("g")
                .attr("class", "segdisplay")
                .attr("transform", "translate(180, 280)")
                .call(segDisplay);

   var segDisplay1 = iopctrl.segdisplay()
                .width(80)  //蓝色数字的宽度
                .digitCount(5)   //蓝色数字的位数
                .negative(false)
                .decimals(0);

        svg.append("g")
                .attr("class", "segdisplay1")
                .attr("transform", "translate(180, 330)")
                .call(segDisplay1);

        svg.append("g")
                .attr("class", "gauge")
                .attr("transform","translate(50,50)")    //位置=两个圆盘半径之差
                .call(gauge);

        svg.append("g")
                .attr("class", "gauge1")
                .call(gauge1);


        segDisplay.value(massage.invest);  //内盘蓝色数字的值,投资数
        segDisplay1.value(massage.result[1]/(massage.invest*10000));  //外盘蓝色数字的值，回报率


        gauge.value(massage.invest/100);   //内盘指针当前指向的值，投资级数
        gauge1.value(massage.result[1]/(massage.invest*10000));   //外盘指针当前指向的值,回报率

     });