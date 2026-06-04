# ZSH 行为与历史
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt hist_ignore_dups hist_ignore_space hist_verify share_history extended_history
setopt auto_cd auto_pushd pushd_ignore_dups
bindkey -e

# zsh-completions 补全路径
fpath=(/opt/zsh/zsh-completions/src $fpath)
autoload -Uz compinit
# 缓存超过 24h 才做安全检查并重建，否则直接用缓存
if [[ -n ~/.zcompdump(#qN.mh+24) ]]; then compinit; else compinit -C; fi
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
zstyle ':completion:*' menu select

# 补全插件
source /opt/zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# starship prompt
eval "$(starship init zsh)"

# zoxide（z 命令跳转目录）
eval "$(zoxide init zsh)"

# 现代 CLI 工具别名
alias ls='eza --icons --group-directories-first'
alias ll='eza -lh --icons --group-directories-first --git'
alias la='eza -lah --icons --group-directories-first --git'
alias lt='eza --tree --icons --level=2'
alias cat='bat --style=plain'
alias find='fd'
alias grep='rg'
