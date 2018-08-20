//液态仪表细节设置
function liquidFillGaugeDefaultSettings() {
    return {
        minValue: 0, // 仪表最小值 ，从数据中传入
        maxValue: 888888888, // 仪表最大值，从数据中传入
        circleThickness: 0.05, //外圆的厚度作为其半径的一个百分比。
        circleFillGap: 0.05, // 外圆与波圈之间的间隙大小为外圆半径的百分比。
        circleColor: "#20B2AA", //外圆的颜色。
        nextcircleColor:"#ca2e33",
        waveHeight: 0.05, //波高作为波圈半径的百分比。
        waveCount: 1, // 波圈每宽度的全波数。
        waveRiseTime: 1000, // 波浪从0上升到最后高度的毫秒时间。
        waveAnimateTime: 18000, //一个完整的波进入波圈的毫秒的时间量。
        waveRise: true, //控制波浪应该从0上升到它的全高，还是从它的全高开始。
        waveHeightScaling: true, //控制波大小缩放在低和高填充百分比。当为真时，波高达到最大值，填充量为50%，最小填充量为0%和100%。这有助于防止波浪在接近最小或最大填充时使波浪圈看起来完全满或空。
        waveAnimate: true, // 控制波浪滚动或静止
        waveColor: "#CDAA7D", // 填充波的颜色。#178BCA
        nextwaveColor:"#4EEE94",
        waveOffset: 0, //最初抵消波浪的量。0＝无偏移。1 =一个完整波的偏移。
        textVertPosition: .5, // 显示波圈的百分比文本的高度。0＝底部，1＝顶部。
        textSize: 1, // 在波圈中显示的文本的相对高度。1＝50%
        valueCountUp: true, // 如果为真，则显示值在加载后从0计数到其最终值。如果为false，则显示最终值。
        displayPercent: true, //如果为真，则在该值之后显示一%个符号。
        textColor: "#812572", // 当波不重叠时，值文本的颜色。  #045681
        nexttextColor: "#ca2e33",
        waveTextColor: "#f8e323", // 当波形重叠时，值文本的颜色。#A4DBf8
        nextwaveTextColor:"#812572",
        piao:"#812572",
        nextpiao:"#812572",
        pingf:"#812572",
        nextping:"#812572",
        value: 0
    };
}
//绑定
function loadLiquidFillGauge(elementId, value, config) {
    if (config == null) config = liquidFillGaugeDefaultSettings();
    var gauge = d3.select("#" + elementId);    //精度
    var radius = Math.min(parseInt(gauge.style("width")), parseInt(gauge.style("height"))) / 2;   //整体圆的半径
    var locationX = parseInt(gauge.style("width")) / 2 - radius;   //x轴
    var locationY = parseInt(gauge.style("height")) / 2 - radius;   //y轴
    var fillPercent = Math.max(config.minValue, Math.min(config.maxValue, value)) / config.maxValue;   //波浪填充百分率计算

    var waveHeightScale;  //波浪高度填充比例
    if (config.waveHeightScaling) {
        waveHeightScale = d3.scale.linear()
            .range([0, config.waveHeight, 0])
            .domain([0, 50, 100]);
    }
    else {
        waveHeightScale = d3.scale.linear()
            .range([config.waveHeight, config.waveHeight])
            .domain([0, 100]);
    }

    var textPixels = (config.textSize * radius / 3.5);       //文字像素
    var textFinalValue = parseFloat(value).toFixed(2);   //文字最终值
    var textStartValue = config.valueCountUp ? config.minValue : textFinalValue;   //文字开始值
    var percentText = config.displayPercent ? "" : "";     //文字所占百分比
    var circleThickness = config.circleThickness * radius;      //圆周厚度
    var circleFillGap = config.circleFillGap * radius;        //环形间隙
    var fillCircleMargin = circleThickness + circleFillGap;  //间隙+圆周厚度
    var fillCircleRadius = radius - fillCircleMargin;        //整个圆的半径
    var waveHeight = fillCircleRadius * waveHeightScale(fillPercent * 100);  //波浪高度

    var waveLength = fillCircleRadius * 2 / config.waveCount;         //波浪长度
    var waveClipCount = 1 + config.waveCount;
    var waveClipWidth = waveLength * waveClipCount;

    //四舍五入函数，以使正确的小数位数总是显示为数值计数。
    var textRounder = function (value) {
        return Math.round(value);
    };
    if (parseFloat(textFinalValue) != parseFloat(textRounder(textFinalValue))) {
        textRounder = function (value) {
            return parseFloat(value).toFixed(1);
        };
    }
    if (parseFloat(textFinalValue) != parseFloat(textRounder(textFinalValue))) {
        textRounder = function (value) {
            return parseFloat(value).toFixed(2);
        };
    }

    //用于构建剪辑波区域的数据。
    var data = [];
    for (var i = 0; i <= 40 * waveClipCount; i++) {
        data.push({x: i / (40 * waveClipCount), y: (i / (40))});
    }

    // 绘制外圆的天平。
    var gaugeCircleX = d3.scale.linear().range([0, 2 * Math.PI]).domain([0, 1]);
    var gaugeCircleY = d3.scale.linear().range([0, radius]).domain([0, radius]);

    // 用于控制剪辑路径大小的刻度。
    var waveScaleX = d3.scale.linear().range([0, waveClipWidth]).domain([0, 1]);
    var waveScaleY = d3.scale.linear().range([0, waveHeight]).domain([0, 1]);

    //用于控制剪辑路径位置的刻度。
    var waveRiseScale = d3.scale.linear()
    // 剪辑区域大小是填充圆的高度+波高，所以我们定位剪辑波。
    // 当它在0%时，它将完全与填充圆重叠，并且将完全覆盖填充物。
    // 100%的圆
        .range([(fillCircleMargin + fillCircleRadius * 2 + waveHeight), (fillCircleMargin - waveHeight)])
        .domain([0, 1]);
    var waveAnimateScale = d3.scale.linear()
        .range([0, waveClipWidth - fillCircleRadius * 2]) // 将剪辑区域推到一个完整的波上，然后回击。
        .domain([0, 1]);

    // 控制仪表内文本位置的刻度。
    var textRiseScaleY = d3.scale.linear()
        .range([fillCircleMargin + fillCircleRadius * 2, (fillCircleMargin + textPixels * 0.7)])
        .domain([0, 1]);

    // 在父SVG内定位轨距。
    var gaugeGroup = gauge.append("g")
        .attr('transform', 'translate(' + locationX + ',' + locationY + ')');

    // 画外圆
    var gaugeCircleArc = d3.svg.arc()
        .startAngle(gaugeCircleX(0))
        .endAngle(gaugeCircleX(1))
        .outerRadius(gaugeCircleY(radius))
        .innerRadius(gaugeCircleY(radius - circleThickness));
    var wcircle = gaugeGroup.append("path")
        .attr("d", gaugeCircleArc)
        .style("fill", config.circleColor)             //外圆颜色
        .attr('transform', 'translate(' + radius + ',' + radius + ')');

    //波不重叠的文本。
    var text1 = gaugeGroup.append("text")
        .text(textRounder(textStartValue) + percentText)
        .attr("class", "liquidFillGaugeText")
        .attr("text-anchor", "middle")
        .attr("font-size", textPixels + "px")
        .style("fill", config.textColor)
        .attr('transform', 'translate(' + radius + ',' + textRiseScaleY(config.textVertPosition) + ')');

    // 削波面积。
    var clipArea = d3.svg.area()
        .x(function (d) {
            return waveScaleX(d.x);
        })
        .y0(function (d) {
            return waveScaleY(Math.sin(Math.PI * 2 * config.waveOffset * -1 + Math.PI * 2 * (1 - config.waveCount) + d.y * 2 * Math.PI));
        })
        .y1(function (d) {
            return (fillCircleRadius * 2 + waveHeight);
        });
    var waveGroup = gaugeGroup.append("defs")
        .append("clipPath")
        .attr("id", "clipWave" + elementId);
    var wave = waveGroup.append("path")
        .datum(data)
        .attr("d", clipArea)
        .attr("T", 0);

    // 内圈与剪辑波相连。
    var fillCircleGroup = gaugeGroup.append("g")
        .attr("clip-path", "url(#clipWave" + elementId + ")")
        .attr("fill", config.waveColor);    //波浪颜色
    fillCircleGroup.append("circle")
        .attr("cx", radius)
        .attr("cy", radius)
        .attr("r", fillCircleRadius);

    // 波浪重叠的文字。
    var text2 = fillCircleGroup.append("text")
        .text(textRounder(textStartValue) + percentText)
        .attr("class", "liquidFillGaugeText")
        .attr("text-anchor", "middle")
        .attr("font-size", textPixels + "px")
        .attr("fill", config.waveTextColor)
        .attr('transform', 'translate(' + radius + ',' + textRiseScaleY(config.textVertPosition) + ')');

    //使价值增值。 初始化text
    if (config.valueCountUp) {
        var textTween = function () {
            var i = d3.interpolate(this.textContent, textFinalValue);
            return function (t) {
                this.textContent = textRounder(i(t)) + percentText;
            }
        };

        text1.transition()
            .duration(config.waveRiseTime)
            .tween("text", textTween);

        text2.transition()
            .duration(config.waveRiseTime)
            .tween("text", textTween)
    }

    //使波浪上升。波和波组是分开的，从而可以独立地控制水平和垂直运动。
    var waveGroupXPosition = fillCircleMargin + fillCircleRadius * 2 - waveClipWidth;
    if (config.waveRise)
    {
        waveGroup.attr('transform', 'translate(' + waveGroupXPosition + ',' + waveRiseScale(0) + ')')
            .transition()
            .duration(config.waveRiseTime)
            .attr('transform', 'translate(' + waveGroupXPosition + ',' + waveRiseScale(fillPercent) + ')')
            .each("start", function () {
                wave.attr('transform', 'translate(1,0)');
            }); // 当waveRise = true且waveAnimate = false时，此变换对于正确定位剪辑波是必要的。没有这个，波浪将无法正确定位，但不清楚为什么这实际上是必要的。 } else {
        waveGroup.attr('transform', 'translate(' + waveGroupXPosition + ',' + waveRiseScale(fillPercent) + ')');
    }

    if (config.waveAnimate) animateWave();

    function animateWave() {
        wave.attr('transform', 'translate(' + waveAnimateScale(wave.attr('T')) + ',0)');
        wave.transition()
            .duration(config.waveAnimateTime * (1 - wave.attr('T')))
            .ease('linear')
            .attr('transform', 'translate(' + waveAnimateScale(1) + ',0)')
            .attr('T', 1)
            .each('end', function () {
                wave.attr('T', 0);
                animateWave(config.waveAnimateTime);
            });
    }
    //更新函数
    function GaugeUpdater() {
        this.update = function (value) {
            var newFinalValue = parseFloat(value).toFixed(2);
            var textRounderUpdater = function (value) {
                return Math.round(value);
            };
            if (parseFloat(newFinalValue) != parseFloat(textRounderUpdater(newFinalValue))) {
                textRounderUpdater = function (value) {
                    return parseFloat(value).toFixed(1);
                };
            }
            if (parseFloat(newFinalValue) != parseFloat(textRounderUpdater(newFinalValue))) {
                textRounderUpdater = function (value) {
                    return parseFloat(value).toFixed(2);
                };
            }

            var textTween = function () {
                var i = d3.interpolate(this.textContent, parseFloat(value).toFixed(2));
                return function (t) {
                    this.textContent = textRounderUpdater(i(t)) + percentText;
                }
            };
            //
            text1.transition()
                .duration(config.waveRiseTime)
                .tween("text", textTween)
                .style("fill",config.nexttextColor);

            text2.transition()
                .duration(config.waveRiseTime)
                .tween("text", textTween)
                .attr("fill",config.nextwaveTextColor);

            wcircle.transition()
                .duration(config.waveRiseTime)
                .style("fill",config.nextcircleColor);

            fillCircleGroup.transition()
                 .duration(config.waveRiseTime)
                 .attr("fill",config.nextwaveColor);

            var fillPercent = Math.max(config.minValue, Math.min(config.maxValue, value)) / config.maxValue;
            var waveHeight = fillCircleRadius * waveHeightScale(fillPercent * 100);
            var waveRiseScale = d3.scale.linear()
            // 剪辑区域大小是填充圆的高度+波高，所以定位剪辑波。
            // 当它在0%时，它将完全与填充圆重叠，并且将完全覆盖填充物。
            // 100%的圆
                .range([(fillCircleMargin + fillCircleRadius * 2 + waveHeight), (fillCircleMargin - waveHeight)])
                .domain([0, 1]);
            var newHeight = waveRiseScale(fillPercent);
            var waveScaleX = d3.scale.linear().range([0, waveClipWidth]).domain([0, 1]);
            var waveScaleY = d3.scale.linear().range([0, waveHeight]).domain([0, 1]);
            var newClipArea;
            if (config.waveHeightScaling) {
                newClipArea = d3.svg.area()
                    .x(function (d) {
                        return waveScaleX(d.x);
                    })
                    .y0(function (d) {
                        return waveScaleY(Math.sin(Math.PI * 2 * config.waveOffset * -1 + Math.PI * 2 * (1 - config.waveCount) + d.y * 2 * Math.PI));
                    })
                    .y1(function (d) {
                        return (fillCircleRadius * 2 + waveHeight);
                    });
            } else {
                newClipArea = clipArea;
            }

            var newWavePosition = config.waveAnimate ? waveAnimateScale(1) : 0;
            wave.transition()
                .duration(0)
                .transition()
                .duration(config.waveAnimate ? (config.waveAnimateTime * (1 - wave.attr('T'))) : (config.waveRiseTime))
                .ease('linear')
                .attr('d', newClipArea)
                .attr('transform', 'translate(' + newWavePosition + ',0)')
                .attr('T', '1')
                .each("end", function () {
                    if (config.waveAnimate) {
                        wave.attr('transform', 'translate(' + waveAnimateScale(0) + ',0)');
                        animateWave(config.waveAnimateTime);
                    }
                });
            waveGroup.transition()
                .duration(config.waveRiseTime)
                .attr('transform', 'translate(' + waveGroupXPosition + ',' + newHeight + ')')


        }
    }

    return new GaugeUpdater();
}
