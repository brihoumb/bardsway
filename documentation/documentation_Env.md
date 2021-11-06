# Bard's Way development environment #
>
> Instruction to install and use the environment of Bard's Way for developing our solution.
>

## Summary: ##
- Requirement
- Install conda
- Configure conda

## Requirement: ##
>
> List of add-on you will need to install before starting the installation.
>

You'll need to install on your own docker, mysql and ffmpeg.  
For some distribution you will also need libavcodec-[dev|devel] and/or ffmpeg-[devel|compta]

## Install conda ##

To start using our environment you need to download miniconda from [here](https://repo.anaconda.com/miniconda/Miniconda3-4.7.10-Linux-x86_64.sh).  
Then run the following ```sh
echo "8a324adcc9eaf1c09e22a992bb6234d91a94146840ee6b11c114ecadafc68121 /path/to/conda.sh" | sha256sum -c```  
When it is over you can run conda.sh and follow he instructions, then reboot your session.

## Configure conda: ##

When conda is downloaded and installed run the following:
```sh
conda create -n bardsway python=3.7.3
conda activate bardsway
pip install -r /path/to/BardsWay/tools/requirement.txt
```  
When you want to work on Bard's Way simply run ```conda activate bardsway```  
When you are done run ```conda deactivate bardsway```
