# oh-my-zsh
export ZSH=/opt/zsh/oh-my-zsh
ZSH_THEME=""
plugins=(git)
source $ZSH/oh-my-zsh.sh

# zsh-completions 的补全路径必须在 compinit 之前加入 fpath
fpath=(/opt/zsh/zsh-completions/src $fpath)

# zsh 补全初始化（须在 fpath 设置之后执行）
autoload -Uz compinit
compinit

# 补全插件
source /opt/zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# starship prompt
eval "$(starship init zsh)"

# zoxide（z 命令跳转目录）
eval "$(zoxide init zsh)"

# 工具别名
alias ls='eza --icons'
alias ll='eza -lh --icons --git'
alias la='eza -lah --icons --git'
alias lt='eza --tree --icons'
alias cat='bat --paging=never'
alias find='fd'
alias grep='rg'
