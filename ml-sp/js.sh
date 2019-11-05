js=$1

jsonnet -V reality=data -V epoch=after -V raw_input_label=tpcrawdecoder:daq \
        -V signal_output_form=sparse \
        -J cfg ${js}.jsonnet \
				-o ${js}.json

wirecell-pgraph dotify --jpath -1 --no-params ${js}.json ${js}.pdf
#wirecell-pgraph dotify --jpath -1 ${js}.json ${js}.pdf
