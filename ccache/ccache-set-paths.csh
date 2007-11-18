if ( "${path}" !~ */usr/libexec/ccache/bin* ) then
        set path = ( /usr/libexec/ccache/bin $path )
endif
