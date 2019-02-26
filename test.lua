package.path = package.path ..";?.lua;test/?.lua;app/?.lua;../?.lua"
require "Pktgen";

function main()
	pktgen.set("1", "rate", "9");
end
main();
