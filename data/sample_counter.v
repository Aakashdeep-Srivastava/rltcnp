module counter (
    input wire clk,
    input wire reset,
    input wire enable,
    output reg [7:0] count,
    output wire max_reached,
    output reg overflow
);

    parameter MAX_COUNT = 8'hFF;
    
    // Counter logic
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            count <= 8'h00;
            overflow <= 1'b0;
        end else if (enable) begin
            if (count == MAX_COUNT) begin
                count <= 8'h00;
                overflow <= 1'b1;
            end else begin
                count <= count + 1'b1;
                overflow <= 1'b0;
            end
        end
    end
    
    // Max reached flag
    assign max_reached = (count == MAX_COUNT) ? 1'b1 : 1'b0;
    
endmodule 